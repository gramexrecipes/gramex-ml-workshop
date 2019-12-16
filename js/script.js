var modelName = null
var trainCols = []
var testSize = "33"
var targetCol = null
var url = g1.url.parse(location.href)
const model_list = {
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

$('#testSize').on('change', (e) => {
  testSize = $('#testSize').val()
  $('#testSizeDisplay').html(`<p>${testSize} %</p>`)
})

$('.formhandler').on('load', function (data) {
  // Show ML section if data is available
  $(data.length) ? $('#mlSection').removeClass('d-none') : $('#mlSection').addClass('d-none');
  let cols = data.meta.columns
  targetCol = cols[cols.length - 1].name
  console.log(`Target column: ${targetCol}`)
  // targetCol = data.meta.columns[0].name

  trainCols = _.filter(data.meta.columns, (c) => {
    return !c.hide
  })
  trainCols = _.map(trainCols, 'name');
  render_target_cols(trainCols);
}).formhandler({
  'pageSize': 5
})

$('#algorithm').on('change', () => {
    modelName = $('#algorithm select').val()
    $('#modelchart').html('')
  })
  .on('load', () => {
    modelName = url.searchKey.model || 'sklearn.linear_model.LogisticRegression'
    url.update({
      model: modelName
    })
    $('#algorithm select').val(modelName)
  })
  .dropdown(model_list)

function render_target_cols(trainCols) {
  $('#targetCol').on('change', () => {
    targetCol = url.searchKey.targetCol
  })
  .dropdown({
    data: trainCols.reverse(),
    target: 'pushState',
    key: 'targetCol'
  })
}

function train() {
  $.ajax({
    url: `train_method`,
    type: 'post',
    data: {
      'model': modelName,
      'url': 'upload_data/data.csv',
      'targetCol': targetCol,
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
