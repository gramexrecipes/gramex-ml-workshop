from gramex.config import variables
from gramex import cache
import os.path as op
from pydoc import locate
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model.base import LinearClassifierMixin
from tornado.template import Template
import json
import joblib

DIR = variables['GRAMEXDATA'] + '/apps/mlhandler'


def init_form(handler):
    """Process input from the landing page and write the current session config."""
    data_file = handler.request.files.get('data-file', [{}])[0]
    # TODO: Unix filenames may not be valid Windows filenames.
    outpath = op.join(DIR, "data.csv")
    with open(outpath, 'wb') as fout:
        fout.write(data_file['body'])
    return 'OK'


class EstimatorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LinearClassifierMixin):
            return {'name': obj.__class__.__name__,
                    'coef_': obj.coef_.tolist()}
        return json.JSONEncoder.default(obj)


def _make_vega(clf, df):
    if isinstance(clf, LinearClassifierMixin):
        with open('linear_model.json', 'r') as fout:
            spec = json.load(fout)
        cdf = pd.DataFrame(clf.coef_, columns=df.columns)
        cdf['class'] = clf.classes_
        cdf = pd.melt(cdf, id_vars='class')
        spec['data']['values'] = cdf.to_dict(orient='records')
    return json.dumps(spec)


def fit(handler):
    model_name = handler.path_args[0]
    if not model_name.endswith('.pkl'):
        model_name += '.pkl'
    kwargs = json.loads(handler.request.body)
    url = kwargs['url'].replace('$GRAMEXDATA', variables['GRAMEXDATA'])
    df = cache.open(url)
    clf = locate(kwargs['model_class'])()
    test_size = float(kwargs['testSize']) / 100
    targetCol = kwargs['output']
    y = df.pop(targetCol).values
    X = df.values
    xtrain, xtest, ytrain, ytest = train_test_split(
            X, y, test_size=test_size, shuffle=True, stratify=y)
    clf.fit(xtrain, ytrain)
    score = clf.score(xtest, ytest)
    path = op.join(DIR, model_name)
    joblib.dump(clf, path)
    with open('report.html', 'r') as fout:
        tmpl = Template(fout.read())
    spec = _make_vega(clf, df)
    return tmpl.generate(score=score, model=clf, spec=spec)
    # return json.dumps({'score': score, 'model': clf}, cls=EstimatorEncoder)
