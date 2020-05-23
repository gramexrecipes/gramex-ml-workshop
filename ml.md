
Lets start with ML code using gramex,

- Write FunctionHandler in `gramex.yaml` to call python code

## Define routes in YAML

```yaml
  scipy-app-modelhandler:
    pattern: /$YAMLURL/train_method
    handler: FunctionHandler
    kwargs:
      function: modelhandler_demo.train_method
      xsrf_cookies: false
      headers:
        Content-Type: text/plain
        Cache-Control: no-store

  #FileHandler to serve generated `chart.png`
  scipy-app-chart:
    pattern: /$YAMLURL/chart.png
    handler: FileHandler
    kwargs:
      path: $YAMLPATH/chart.png
      headers:
        Cache-Control: no-store
```

- Write Python code to `application_name.py` file and import your ml libraries

## Python imports

```py
import json
from pydoc import locate

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gramex import cache
from scipy.stats import norm
from sklearn import naive_bayes as nb
from sklearn.linear_model.base import LinearClassifierMixin
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from tornado.template import Template
```

## Define routes in YAML
```py
def train_method(handler):
    """Training, testing method."""
    url = handler.get_argument('url', default='upload_data/data.csv')
    df = cache.open(url)

    # read variables adjusted in the UI
    clf = locate(handler.get_argument('model_class'))()
    test_size = float(handler.get_argument('testSize')) / 100
    target_col = handler.get_argument('output')

    dfy = df[target_col]
    dfx = df[[c for c in df if c != target_col]]
    x, y = dfx.values, dfy.values

    # train, test split, fit, determine accuracy
    xtrain, xtest, ytrain, ytest = train_test_split(
            x, y, test_size=test_size, shuffle=True, stratify=y)
    clf.fit(xtrain, ytrain)
    score = clf.score(xtest, ytest)

    # write back the output to report.html, custom tornado template
    with open('report.html', 'r', encoding='utf8') as fout:
        tmpl = Template(fout.read())
    viz = _make_chart(clf, dfx)
    return tmpl.generate(score=score, model=clf, spec=viz)
```

- generate interactive and static charts

```py
def _make_gnb_chart(clf, dfx):
    plt.close('all')

    n_classes, n_feats = clf.theta_.shape
    std = np.sqrt(clf.sigma_)
    fig, ax = plt.subplots(nrows=n_classes, ncols=n_feats, sharex=True)
    for i in range(n_classes):
        for j in range(n_feats):
            loc = clf.theta_[i, j]
            scale = std[i, j]
            p = norm(loc, scale)
            x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 100)  # noqa: E912
            y = p.pdf(x)
            ax[i, j].plot(x, y)
            ax[i, j].fill_between(x, y, where=y > 0)
            if i < (n_classes - 1):
                ax[i, j].tick_params(axis='x', bottom=False)
    for i, _ax in enumerate(ax[:, -1]):
        _ax.set_ylabel(clf.classes_[i])
        _ax.yaxis.set_label_position('right')
    for i, _ax in enumerate(ax[0, :]):
        _ax.set_xlabel(dfx.columns[i])
        _ax.xaxis.set_label_position('top')
    plt.tight_layout()
    plt.savefig('chart.png')


def _plot_decision_tree(clf, dfx):
    plt.close('all')
    fig, ax = plt.subplots()
    plot_tree(clf, filled=True, ax=ax)
    plt.savefig('chart.png')


def _make_chart(clf, df):
    if isinstance(clf, (LinearClassifierMixin, nb.MultinomialNB)):
        with open('chart_spec.json', 'r', encoding='utf8') as fout:
            spec = json.load(fout)
        cdf = pd.DataFrame(clf.coef_, columns=df.columns)
        cdf['class'] = clf.classes_
        cdf = pd.melt(cdf, id_vars='class')
        spec['data']['values'] = cdf.to_dict(orient='records')
        return json.dumps(spec)
    if isinstance(clf, nb.GaussianNB):
        _make_gnb_chart(clf, df)
        return True
    if isinstance(clf, DecisionTreeClassifier):
        _plot_decision_tree(clf, df)
        return True
    return False

```

- Create `report.html` file and add scaffolding

```html
{% if score < 0.5 %}
  {% set tcls = 'text-danger' %}
{% elif score < 0.7 %}
  {% set tcls = 'text-warning' %}
{% elif score >= 0.7 %}
  {% set tcls = 'text-success' %}
{% end %}

<div class="container-fluid">
  <div class="row">
    <div class="h1 text-center">
      Your model scored <span class="{{ tcls }}">{{ '{:.2%}'.format(score) }}</span>
    </div>
  </div>
  <div class="row">
    <div id="modelchart"></div>
  </div>
</div>

{% if spec %}
<script>
  {% import json %}
  {% try %}
    {% set specs = json.loads(spec) %}
    {% autoescape None %}
    {% from tornado.escape import json_decode %}
    var spec = {{ spec }}
    var view = new vega.View(vega.parse(vegaLite.compile(spec).spec))
        .renderer('svg')
        .initialize('#modelchart')
        .hover()
        .run()
  {% except (json.JSONDecodeError, TypeError) %}
    $('#modelchart').html('<img src="chart.png"/>')
  {% end %}

</script>
{% end %}

```

# Trigger your python code using jQuery
- create `js/script.js` file and add below lines

```js
var modelName = null
var trainCols = []
var testSize = $('.custom-range').val()
var targetCol = null
var url = g1.url.parse(location.href)
const modelist = {
  data: [{
      'label': 'Logistic Regression',
      'value': 'sklearn.linear_model.LogisticRegression'
    },
    {
      'label': 'Perceptron',
      'value': 'sklearn.linear_model.Perceptron'
    },
    {
      'label': 'PAC',
      'value': 'sklearn.linear_model.PassiveAggressiveClassifier'
    },
    {
      'label': 'SVC',
      'value': 'sklearn.svm.SVC'
    },
    {
      'label': 'Nu-SVC',
      'value': 'sklearn.svm.NuSCV'
    },
    {
      'label': 'Linear SVC',
      'value': 'sklearn.svm.LinearSVC'
    },
    {
      'label': 'Nearest Neighbors',
      'value': 'sklearn.neighbors.KNeighborsClassifier'
    },
    {
      'label': 'Gaussian NB',
      'value': 'sklearn.naive_bayes.GaussianNB'
    },
    {
      'label': 'Bernoulli NB',
      'value': 'sklearn.naive_bayes.BernoulliNB'
    },
    {
      'label': 'Multinomial NB',
      'value': 'sklearn.naive_bayes.MultinomialNB'
    },
    {
      'label': 'Decision Tree',
      'value': 'sklearn.tree.DecisionTreeClassifier'
    },
    {
      'label': 'Random Forests',
      'value': 'sklearn.ensemble.RandomForestClassifier'
    },
    {
      'label': 'Neural Networks',
      'value': 'sklearn.neural_network.MLPClassifier'
    }
  ],
  value_key: 'value',
  label_key: 'label',
  target: 'pushState',
  key: 'model'
};

$('.formhandler').on('load', function (data) {
  // Show ML section if data is available
  $(data.length) ? $('#mlSection').removeClass('d-none') : $('#mlSection').addClass('d-none');

  trainCols = _.filter(data.meta.columns, (c) => {
    return !c.hide
  })
  trainCols = _.map(trainCols, 'name');
  render_tc_dd(trainCols);
}).formhandler({
  'pageSize': 5
})

$('#algorithm').on('change', () => {
    modelName = url.searchKey.model
    $('#modelchart').html('')
  })
  .on('load', () => {
    modelName = 'sklearn.linear_model.LogisticRegression'
    url.update({
      model: modelName
    })
  })
  .dropdown(modelist)

function render_tc_dd(trainCols) {
  $('#targetCol').on('change', () => {
      targetCol = url.searchKey.targetCol
    })
    .dropdown({
      data: trainCols,
      target: 'pushState',
      key: 'targetCol'
    })
}

function train() {
  $.ajax({
    url: `train_method`,
    type: 'post',
    headers: {
      'Model-Retrain': true
    },
    data: {
      'model_class': modelName,
      'url': 'upload_data/data.csv',
      'output': targetCol,
      'testSize': testSize,
    },
    success: (data) => {
      $('#report').html(data)
    }
  })
}

$('#train').on('click', () => {
  // On click of Train button trigger 
  train()
})

```

# To add interactive charts use [vega](https://vega.github.io/vega/)
create `chart_spec.json` add below vega code.

```json
{
	"width": 360,
	"height": 270,
	"$schema": "https://vega.github.io/schema/vega-lite/v3.json",
	"encoding": {
    "y": {"field": "variable", "type": "nominal"},
    "x": {"field": "class", "type": "nominal"}
	},
	"layer": [
    {
      "mark": "rect",
      "selection": {"brush": {"type": "interval"}},
      "encoding": {
        "color": {"field": "value", "type": "quantitative"}
      }
    },
    {
      "mark": "text",
      "encoding": {
        "text": {"field": "value", "type": "quantitative"}
      }
    }
	],
  "data": {
    "name": "coef_",
    "values": ""
  }
}
```

In case of any query feel free to reach out.
- Jaidev Deshpande <jaidev.deshpande@gramener.com>
- Nivedita Deshmukh <nivedita.deshmukh@gramener.com>
- Kamlesh Jaiswal <kamlesh.jaiswal@gramener.com>
