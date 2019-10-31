from gramex.config import variables
import numpy as np
from base64 import b64encode
from gramex import cache
import os.path as op
from pydoc import locate
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model.base import LinearClassifierMixin
from sklearn import naive_bayes as nb
from tornado.template import Template
import json
import joblib
import matplotlib.pyplot as plt
import tempfile
from scipy.stats import norm, multinomial, bernoulli

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


def _plot_nb(clf, dfX):
    if isinstance(clf, nb.GaussianNB):
        N = norm
    elif isinstance(clf, nb.MultinomialNB):
        N = multinomial
    else:
        N = bernoulli
    plt.close('all')
    n_classes, n_feats = clf.theta_.shape
    std = np.sqrt(clf.sigma_)
    fig, ax = plt.subplots(nrows=n_classes, ncols=n_feats)
    for i in range(n_classes):
        for j in range(n_feats):
            loc = clf.theta_[i, j]
            scale = std[i, j]
            p = N(loc, scale)
            x = np.linspace(N.ppf(0.01), N.ppf(0.99), 100)
            ax[i, j].plot(x, p.pdf(x))
    plt.tight_layout()
    return fig, ax


def _make_nb_charts(clf, dfX):
    fig, ax = _plot_nb(clf, dfX)
    with tempfile.TemporaryFile() as tf:
        fig.savefig(tf, format='png')
        tf.seek(0)
        spec = tf.read()
    return spec


def _make_chart(clf, df):
    if isinstance(clf, LinearClassifierMixin):
        with open('linear_model.json', 'r') as fout:
            spec = json.load(fout)
        cdf = pd.DataFrame(clf.coef_, columns=df.columns)
        cdf['class'] = clf.classes_
        cdf = pd.melt(cdf, id_vars='class')
        spec['data']['values'] = cdf.to_dict(orient='records')
    elif isinstance(clf, nb.BaseNB):
        spec = _make_nb_charts(clf, df)
    else:
        spec = False
    if isinstance(spec, bytes):
        return b64encode(spec)
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
    dfy = df[targetCol]
    dfX = df[[c for c in df if c != targetCol]]
    X, y = dfX.values, dfy.values
    xtrain, xtest, ytrain, ytest = train_test_split(
            X, y, test_size=test_size, shuffle=True, stratify=y)
    clf.fit(xtrain, ytrain)
    score = clf.score(xtest, ytest)
    path = op.join(DIR, model_name)
    joblib.dump(clf, path)
    with open('report.html', 'r') as fout:
        tmpl = Template(fout.read())
    viz = _make_chart(clf, dfX)
    return tmpl.generate(score=score, model=clf, spec=viz)
    # return json.dumps({'score': score, 'model': clf}, cls=EstimatorEncoder)
