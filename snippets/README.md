# Snippets

Snippets directory provides minimal utilites to build a simple web page for the workshop.

# Application Components

## Structure

- snippets
  - base.html
  - upload.html
  - table.html
  - training.html
  - curated.html
  - README.md

## Build your application

every `HTML` file below can be rendered by requesting for

http://localhost:9988/snippets/base or

http://localhost:9988/snippets/upload_file or 

http://localhost:9988/snippets/table or

http://localhost:9988/snippets/training or

http://localhost:9988/snippets/curated

Each view below builds on top of the previous step. Table of contents is as follows:

- [Step 0 - curated.html](#step-0---curatedhtml)
- [Step 1 - base.html](#step-1---basehtml)
- [Step 2 - upload.html](#step-1---uploadhtml)
- [Step 3 - base.html](#step-1---basehtml)
- [Step 4 - table.html](#step-1---tablehtml)
- [Step 5 - training.html](#step-1---traininghtml)

### Step 0 - curated.html

We'll create this `curated.html` using the steps defined below.

### Step 1 - base.html

Begin with base.html, you'll a navbar (header for the page).

The corresponding `YAML` routing (found in [gramex.yaml](../gramex.yaml)) is as below:

```yaml
  workshop/snippets/base:
    pattern: /$YAMLURL/snippets/base
    handler: FileHandler
    kwargs:
      path: $YAMLPATH/snippets/base.html
      template: true
```

Your page should now look like below

![base html](images/base.png)

### Step 2 - upload.html

In `base.html`, add the content from `upload.html`.

The corresponding `YAML` routing (found in [gramex.yaml](../gramex.yaml)) is as below:

```yaml
  workshop/snippets/upload:
    pattern: /$YAMLURL/snippets/upload_file
    handler: FileHandler
    kwargs:
      path: $YAMLPATH/snippets/upload.html
      template: true
```

Your page should now look like below

![base + upload html](images/upload.png)

### Step 3 - table.html

We rely on a table renderer from `g1` library named `formhandler table`.

For it to work, we need to integrate few lines of `JavaScript`.

```html
<script src="../ui/jquery/dist/jquery.min.js"></script>
<script src="../ui/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="../ui/lodash/lodash.min.js"></script>
<script src="../ui/g1/dist/g1.min.js"></script>
<script>
  // '.formhandler' is the div element in `table.html`
  $('.formhandler').formhandler({
    pageSize: 5
  })
</script>
```

The corresponding `YAML` routing (found in [gramex.yaml](../gramex.yaml)) is as below:

```yaml
  workshop/snippets/table:
    pattern: /$YAMLURL/snippets/table
    handler: FileHandler
    kwargs:
      path: $YAMLPATH/snippets/table.html
      template: true
```

also note that rendering the table relies on `data` endpoint in [gramex.yaml](../gramex.yaml):

```yaml
  formhandler:
    pattern: /$YAMLURL/snippets/data
    handler: FormHandler
    kwargs:
      url: $YAMLPATH/upload_data/data.csv
```

Your page should now look like below

![base + upload + table html](images/table.png)

To know more about g1's formhandler table, visit https://learn.gramener.com/guide/g1/.

### Step 4 - training.html

Your page should now look like below

![base + upload + table + training html](images/training.png)

## Interactions

Let's now discuss how the application will function interactively (on user input). User can:

- [upload a file](#file-upload)
  - upon which table is updated
  - `Tweak the parameters` section is updated
  - and model can be trained
- [Train the model](#train-the-model)

### File upload

Gramex handles any file uploads via `UploadHandler` with several out-of-the-box features (overwriting, replacement, redirection etc.).

```yaml
  uploadhandler:
    pattern: /$YAMLURL/snippets/upload_file
    handler: UploadHandler
    kwargs:
      if_exists: overwrite            # Overwrite the original without backup
      path: $YAMLPATH/upload_data
  # this will show the output post file uploading
```

### Train the model

Note the attributes that change he selections in `Tweak the parameters` section.

| Type | Values | Notes |
| ---- | ------ | ----- |
| Select target columns | List of features from data | Categorical variables will be used for the workshop. |
| Select test size      | Dataset % as test size, 0 to 100% | Change it to see how model accuracy varies! |
| Select algorithm | List of features from data, algorithm to train with |Note that model accuracy is applicable to linear models alone, for the rest it's not implemented for this workshop. |

#### Target selection
To populate the values in `Select Algorithm` select option, refer to the variable `model_list` in `js/script.js`.

#### Algorithm selection
To populate the values in `Select Algorithm` select option, refer to the variable `model_list` in `js/script.js`.

```js
{
  'label': 'Logistic Regression',
  'value': 'sklearn.linear_model.LogisticRegression'
}
```
where `label` is what is shown in the `select` option while `sklearn.linear_model.LogisticRegression` is its value.

#### Training 

![training submission](images/train.png)

Clicking on `Train` button makes an `AJAX` request. If you aren't familiar with it, that's fine. It's a mechanism to retrieve information from server asynchronously.

```js
function train() {
  $.ajax({
    url: 'train_method',    // train_method is a route in gramex.yaml
    type: 'post',           // makes a POST request
    data: {
      'model': modelName,
      'url': 'upload_data/data.csv',
      'targetCol': targetCol,
      'testSize': testSize,
    },
    success: (response_data) => {
      // response is rendered in `report.html` that has div#report element
      $('#report').html(response_data)
    }
  })
}
```

observe the `train_method` route defined in `url` attribute in `$.ajax` above defined in the YAML configuration below...

that's how requests are routed from front-end to back-end.

```yaml
# snippet for `train_method` endpoint in gramex.yaml
modelhandler:
  pattern: /$YAMLURL/train_method
  handler: FunctionHandler
  kwargs:
    # runs train_method() function in modelhandler_demo.py
    function: modelhandler_demo.train_method
```

The key aspects of the back-end (`python`) are:

- URL parameter retrieval

```py
url = handler.get_argument('url')
clf = locate(handler.get_argument('model'))()
test_size = float(handler.get_argument('testSize')) / 100
target_col = handler.get_argument('targetCol')
```

- training/test data split, fit to classifier and determine accuracy

```py
# train/test data split, fit to classifier and determine accuracy
xtrain, xtest, ytrain, ytest = train_test_split(
        x, y, test_size=test_size, shuffle=True, stratify=y)
clf.fit(xtrain, ytrain)
score = clf.score(xtest, ytest)
```

- send the output to front-end (`JavaScript`)

```py
with open(op.join(YAMLPATH, 'report.html'), 'r', encoding='utf8') as fout:
    tmpl = Template(fout.read())
viz = _make_chart(clf, dfx)
return tmpl.generate(score=score, model=clf, spec=viz)
```

## Final output

Your page should now look like below

![final-output](images/final.png)

If it doesn't, don't worry. Look at the content in `final.html` and replicate it or copy/paste it.
