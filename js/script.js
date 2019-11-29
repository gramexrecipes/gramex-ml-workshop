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
    success: (response_data) => {
      $('#report').html(response_data)
    }
  })
}

$('#train').on('click', () => {
  train()
})
