Building ML Applications with Gramex
===================================

## Setup

- [Installation guide](https://code.gramener.com/nivedita.deshmukh/gramex-scipy-workshop/blob/master/installation_guide.md)  Note: URL needs to be updated

# Part 1: Gramex as an HTTP Server

## Gramex init
To create an empty project, run `gramex init` inside your project directory on your terminal.
```
$ gramex init
```

It generates a simple boilerplate:
- `gramex.yaml`: Gramex [configuration](https://learn.gramener.com/guide/config/)
- `index.html`: default home page
- `README.md`: project documentation

… and a set of configurations that help development.
- `.gitignore` [info](https://git-scm.com/docs/gitignore)
- `.gitlab-ci.yml` [info](https://docs.gitlab.com/ce/ci/yaml/)


Navigate to the project folder through the terminal or the command prompt, and run Gramex as follows:

```bash
$ gramex
```

When gramex starts running, you should be able to see some output logs. When you see the following lines,

```
INFO    22-Apr 13:34:26 __init__ PORT Listening on port 9988
INFO    22-Apr 13:34:26 __init__ 9988 <Ctrl-B> opens the browser. <Ctrl-D> starts the debugger.
```

the gramex server is ready to serve the application.

Please visit [`http://localhost:9988`](http://localhost:9988) in your browser. If you see a web page which looks something like the following screenshot, you are ready for the workshop.

![](assets/screen.png)


## App configuration
The `app:` section controls Gramex’s startup. It has these sub-sections.
```diff
app:
    listen:
        port: 8888
    settings:
        debug: True
    browser: '/'
```
1. `browser:` is the URL to open when Gramex is launched. (default: False)
2. `listen:` holds keyword arguments for the HTTP server. The most important parameter is the port: (default: 9988.) The remaining parameters are passed to HTTPServer().
3. `settings:` holds the Tornado application settings.
4. `debug:` holds the debug settings

## URL mapping
The `url:` section maps URLs to content. Here is an example:
```
url:
    home:                                   # "homepage" can be replaced with any unique name
        pattern: /$YAMLURL/                 # Map the URL /
        handler: FileHandler                # using a built-in FileHandler
        kwargs:                             # Pass these options to FileHandler
            path: $YAMLPATH/home.html       # Use index.html as the path to serve
            template: true                  # rendered as a Tornado template

    hello:                                  # A unique name for this mapping
        pattern: /hello                     # Map the URL /hello
        handler: FunctionHandler            # using the build-in FunctionHandler
            kwargs:                         # Pass these options to FunctionHandler
                function: str("Hello")      # Run the str() function with the argument "Hello"
```
The `url:` section is a name - mapping dictionary. The names are just unique identifiers. The mappings have these keys:
- `pattern:` a regular expression that matches the URL. For example, `/blog/(.*)` matches all pages starting with `/blog/.` Any parts of the URL in brackets are passed to the handler as arguments.
- `handler:` The name of the Tornado RequestHandler to run. Gramex provides many handlers by default. Here are some commonly used ones:
    - `FunctionHandler:` runs any function and renders the output
    - `FileHandler:` transforms & displays files
    - `UploadHandler:` lets you upload files and manage them 
    - `FormHandler:` lets you read & write data from files and databases
- `kwargs:` Keyword arguments to pass to the handler. The arguments varies by handler.

# Part 2: Data Management
## FileHandler
`gramex.yaml` uses the `FileHandler` to display files. This folder uses the following configuration:
```
scipy-app-home:
    pattern: /$YAMLURL/
    handler: FileHandler
    kwargs:
      path: $YAMLPATH/index.html
      template: true
```
`$YAMLURL` is replaced by the current URL’s path (in this case, `/filehandler/`) and `$YAMLPATH` is replaced by the directory of `gramex.yaml`.

### index.html
...

## FunctionHandler
The `FunctionHandler` runs a function and displays the output. For example, this configuration maps the URL `total` to a FunctionHandler:
```
url:
    total:
        pattern: /$YAMLURL/total                    # The "total" URL
        handler: FunctionHandler                    # runs a function
        kwargs:
            function: calculations.total(100, 200)  # total() from calculations.py
            headers:
                Content-Type: application/json      # Display as JSON
```
It runs `calculations.total()` with the arguments `100, 200` and returns result `300` as `application/json.` calculations.py defines `total` as below:
```
def total(*items):
    return json.dumps(sum(float(item) for item in items))
```

## UploadHandler
`UploadHandler` lets you upload files and manage them. Here is a sample configuration:
```
scipy-app-uploadhandler:
    pattern: /$YAMLURL/upload
    handler: UploadHandler
    kwargs:
        if_exists: overwrite      # Overwrite the original without backup
        # if_exists: error        # Raises a HTTP 403 with a reason saying "file exists"
        # if_exists: backup       # Move the original to filename.YYYYMMDD-HHMMSS.ext
        # if_exists: unique       # Save to a new file: filename.1, filename.2, etc
        path: $YAMLPATH/upload_data
        # methods: get              # Upload listing
        redirect: /$YAMLURL/    # redirect to url
```
By default, `.meta.db` keystore is created in `kwargs:path` directory to store uploaded files’ metadata.

Any file posted with a name of file is uploaded. Here is a sample HTML form:
```
  <form action="upload" method="POST" enctype="multipart/form-data">
    <input name="file" type="file">
    <button type="submit">Submit</button>
    <input type="hidden" name="_xsrf" value="{{ handler.xsrf_token }}">
    <input type="hidden" name="save" value="data.csv">
  </form>
```

## FormHandler
`FormHandler` lets you read & write data from files and databases
Here is a sample configuration to read data from a CSV file:

```
  scipy-app-formhandler:
    pattern: /$YAMLURL/data
    handler: FormHandler
    kwargs:
      url: $YAMLPATH/upload_data/data.csv
```

You can read from a HTTP or HTTPS URL.

```
    # This URL is read once and cached forever
    url: https://learn.gramener.com/guide/formhandler/flags.csv
    ext: csv          # Explicitly specify the extension for HTTP(S) urls
```

```
FormHandler filters
The URL supports operators for filtering rows. The operators can be combined.

?Continent=Europe ► Continent = Europe
?Continent=Europe&Continent=Asia ► Continent = Europe OR Asia. Multiple values are allowed
?Continent!=Europe ► Continent is NOT Europe
?Continent!=Europe&Continent!=Asia ► Continent is NEITHER Europe NOR Asia
?Shapes ► Shapes is not NULL
?Shapes! ► Shapes is NULL
?c1>=10 ► c1 > 10 (not >= 10)
?c1>~=10 ► c1 >= 10. The ~ acts like an =
?c1<=10 ► c1 < 10 (not <= 10)
?c1<~=10 ► c1 <= 10. The ~ acts like an =
?c1>=10&c1<=20 ► c1 > 10 AND c1 < 20
?Name~=United ► Name matches &_format=html
?Name!~=United ► Name does NOT match United
?Name~=United&Continent=Asia ► Name matches United AND Continent is Asia
```


# Part 3: Files and Templates
## Redirection and Templates
### Redirection
Most URL handlers (not all) accept a `redirect:` parameter that redirects the user after completing the action. For example, after an `UploadHandler` is done. Here is the syntax:
```
uploadhandler:
    pattern: /$YAMLURL/upload
    handler: UploadHandler
    kwargs:
        if_exists: overwrite
        path: $YAMLPATH/upload_data
        redirect: /$YAMLURL/show-data       # redirects on the url /show-data which defined below
```
NOTE: You can only redirect pages that don’t return any content.

### Templates
The `template` configuration renders files as `Tornado templates`. To serve a file as a Tornado template, use the following configuration:
```
templates:
    pattern: /$YAMLURL/show-data
    handler: FileHandler                    # displays a file
    kwargs:
        path: $YAMLPATH/reports.html        # named reports.html
        template: true                      # rendered as a Tornado template
```

Template files can contain any template feature. Here’s a sample `reports.html`.
```html
{% import os %}
{% import json %}
{% import pandas as pd %}
{% import gramex.cache as gxc %}
{% set args = handler.get_argument %}
{% import gramex.handlers.uploadhandler %}
{% set uploader = gramex.handlers.uploadhandler.FileUpload('./upload_data').info() %}

<h1 align="center"> {{list(uploader.values())[-1]['filename']}} </h1>
<br>
{% set file_name = list(uploader.values())[-1]['filename'] %}
{% set file_path = os.path.join(gramex.config.variables['$YAMLPATH'], 'upload_data') %}
<!-- <p>{{args('curr_file', 'NO')}}</p> -->
{% set data = pd.read_csv('{0}/{1}'.format(file_path, file_name), encoding='utf-8') %}
{% set data_dic = data.to_dict(orient='records') %}
{% set col_li = list(data_dic[0].keys()) %}
<div>
  <table border="1">
    <thead>
      <tr>
        {% for col in col_li %}
          <th>{{col}}</th>
        {% end %}
      </tr>
    </thead>
    <tbody>
      {% for i, d in enumerate(data_dic) %}
        <tr>
          {% for c in col_li %}
            <td>{{d[c]}}</td>
          {% end %}
        </tr>
      {% end %}
    </tbody>
  </table>
</div>
```
# Part 4: Putting it all together
..

## Contributions

- Nivedita Deshmukh <nivedita.deshmukh@gramener.com>
- Kamlesh Jaiswal <kamlesh.jaiswal@gramener.com>
- Jaidev Deshpande <jaidev.deshpande@gramener.com>