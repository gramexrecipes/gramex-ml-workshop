Building ML Applications with Gramex
===================================

## Setup and Installation

- [Installation guide](https://github.com/kamleshdjango/gramex-ml-workshop/blob/scipy-workshop/installation_guide.md)


Getting Started with Gramex
============================

# Part 1: Gramex as an HTTP Server

## Gramex init
Run `gramex init` on your terminal.

```bash
$ gramex init
```
It generates a simple boilerplate:

- `gramex.yaml`: Gramex configuration
- `index.html`: default home page
- `README.md`: project documentation

… and a set of configurations that help development.
- `.gitignore`      # Ignores a set of various files 
- `.gitlab-ci.yml`  # The `.gitlab-ci.yml` file tells the GitLab Runner what to do.
                    # `gramex init` will created it with configure your GitLab project to use a Runner.
                    # On any push to your repository, GitLab will look for the .gitlab-ci.yml file and start jobs on Runners according to the contents of the file, for that commit.

Open a terminal, navigate to the project folder and run Gramex as follows:

```bash
$ gramex
```
When gramex starts running, you should be able to see some output logs. When you see the following lines,
gramex start on default port `9988`

```
INFO    22-Apr 13:34:26 __init__ PORT Listening on port 9988
INFO    22-Apr 13:34:26 __init__ 9988 <Ctrl-B> opens the browser. <Ctrl-D> starts the debugger.
```

the gramex server is ready to serve the application.

Please visit [`http://localhost:9988`](http://localhost:9988) in your browser. If you see a web page which looks something like the following screenshot, you are ready for the workshop.

![](assets/screen.png)

## App configuration

The `app:` section controls Gramex’s startup. It has these sub-sections.

```yaml
app:
    listen:
        port: 9987
    settings:
        debug: False
    browser: '/'
```

1. `browser:` is the URL to open when Gramex is launched. (default: False)
2. `listen:` holds keyword arguments for the HTTP server. The most important parameter is the port: (default: 9988.) The remaining parameters are passed to HTTPServer().
3. `settings:` holds the Tornado application settings.
4. `debug:` holds the debug settings

# YAML imports

One config file can import another. For example:

```yaml
import:
  ui:
    path: $GRAMEXAPPS/ui/gramex.yaml   # import this YAML file relative to current file path
    YAMLURL: $YAMLURL/ui/
```

## URL mapping
In order to provide our app with access to the data, we need to create a URL that sends data to the app.
The `url:` section maps URLs to content. Here is an example:

```yaml
url:
    appname-home:                                   # "homepage" can be replaced with any unique name
        pattern: /$YAMLURL/                 # Map the URL /
        handler: FileHandler                # using a built-in FileHandler
        kwargs:                             # Pass these options to FileHandler
            path: $YAMLPATH/index.html      # Use index.html as the path to serve
            template: true                  # rendered as a Tornado template

    appname-hello:                                  # A unique name for this mapping
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

```yaml
appname-home:
    pattern: /$YAMLURL/
    handler: FileHandler
    kwargs:
      path: $YAMLPATH/index.html      # Serve files from this YAML file's directory
      template: true
```

`$YAMLURL` is replaced by the current URL’s path (in this case, `/filehandler/`) and `$YAMLPATH` is replaced by the directory of `gramex.yaml`.

### index.html
<h1>Say Hello Gramex.</h1>

## FunctionHandler
The `FunctionHandler` runs a function and displays the output. For example, this configuration maps the URL `total` to a FunctionHandler:

```yaml
url:
    # FunctionHandler using yaml
    hello:                                        # A unique name for this mapping
        pattern: /$YAMLURL/hello                  # Map the URL /hello
        handler: FunctionHandler                  # using the build-in FunctionHandler
        kwargs:                                   # Pass these options to FunctionHandler
            function: str('Hello Gramex')         # Run the str() function with the argument "Hello Gramex"
    
    # FunctionHandler with python file
    total:
        pattern: /$YAMLURL/total                    # The "total" URL
        handler: FunctionHandler                    # runs a function
        kwargs:
            function: modelhandler.total(100, 200)    # total() from modelhandler.py
            headers:
                Content-Type: application/json      # Display as JSON
```

It runs `modelhandler.total()` with the arguments `100, 200` and returns result `300` as `application/json.` modelhandler.py defines `total` as below:
Create python `file app_scrpt.py` in your project directory and write a below function.

```python
import json
def total(*items):
    return json.dumps(sum(float(item) for item in items))
```

### URL path arguments
You can specify wildcards in the URL pattern. For example:
place in `.yaml` following.

```yaml
app-lookup:
    pattern: /$YAMLURL/name/([a-z]+)/age/([0-9]+)        # e.g. /name/john/age/21
    handler: FunctionHandler                             # Runs a function
    kwargs:
        function: modelhandler.name_age                    # Run this function
```

When you access `/name/john/age/21`, `john` and `21` can be accessed via handler.path_args as follows:
place in `.py` follwing code

```python
def name_age(handler):
    """URL path arguments."""
    name = handler.path_args[0]
    age = handler.path_args[1]
    return json.dumps({"Name": name, "Age": age})
```

## UploadHandler

`UploadHandler` lets you upload files and manage them. Here is a sample configuration:

```yaml
app-uploadhandler:
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

```yaml
  appname-formhandler:
    pattern: /$YAMLURL/data
    handler: FormHandler
    kwargs:
      url: $YAMLPATH/upload_data/data.csv
```

You can read from a HTTP or HTTPS URL.

```yaml
    # This URL is read once and cached forever
    url: https://learn.gramener.com/guide/formhandler/flags.csv
    ext: csv          # Explicitly specify the extension for HTTP(S) urls
```

- FormHandler filters

```
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

- FormHandler formats
```
By default, FormHandler renders data as JSON. Use ?_format= to change that.

Default: flags
HTML: flags?_format=html
CSV: flags?_format=csv
JSON: flags?_format=json
XLSX: flags?_format=xlsx
Table: flags?_format=table from v1.23 - an interactive table viewer
```
To include the table format, you must include this in your gramex.yaml:
```
import:
  path: $GRAMEXPATH/apps/formhandler/gramex.yaml
  YAMLURL: $YAMLURL         # Mount this app at the current folder
```

## Smart alert 
The alert service sends reports via email.
First, set up an `email service`. Here is a sample:
```
email:
  gramex-guide-gmail:
    type: gmail                       # Type of email used is GMail
    email: gramex.guide@gmail.com     # Generic email ID used to test e-mails
    password: tlpmupxnhucitpte        # App-specific password created for Gramex guide
```
### Alert Example
```
Email scheduling uses the same keys as scheduler: `minutes`, `hours`, `dates`, `weekdays`, `months` and `years`.
alert:
  alert-schedule:
    # days: '*'                       # Send email every day
    # hours: '6, 12'                  # at 6am and 12noon
    # minutes: 0                      # at the 0th minute, i.e. 6:00am and 12:00pm
    startup: false
    # condition: once("Hello World!")
    to:
      - user.name@email.com
    cc: user.name@email.com
    subject: Scheduled alert
    body: This email will be scheduled and sent as long as Gramex is running.
    # html: <p>This content will be shown in <em>HTML</em> on <strong>supported devices</strong>.
    # markdown: |
    #   <p>This email has inline images.</p>
    #   <img src="cid:img1">
    # markdownfile: $YAMLPATH/content.md
    # images:
    #  img1: $YAMLPATH/required_sequence.png
    # attachments:
    #  - map_data.xlsx
```
- To send an email on `startup`, use startup: instead of `days:`, `hours:`, etc. This sends an email every time Gramex starts.
- To avoid resentding email, condition: once(..) ensures that an alert campaign is sent out only once. once() returns boolean.
- `html:` specifies the HTML content to be sent.
- `markdown:` can be used to specify the HTML content as Markdown instead of html (and overrides it).
- `markdownfile:` place in markdownfile instead and pass file name
here `content.md` file to attach in markdown.
```
<p>This email has inline images.</p>
<img src="cid:img1">
```

# Part 3: Security
## Authentication
Gramex allows users to log in using various single sign-on methods.
- Define a Gramex auth handler. This URL renders / redirects to a login page
- When the user logs in, send the credentials to the auth handler
- If credentials are valid, store the user details and redirect the user. Else show an error message.
This configuration creates a `simple auth` page:
```
login/simple:
    pattern: /$YAMLURL/simple           # Map this URL
    handler: SimpleAuth                 # to the SimpleAuth handler
    kwargs:
        credentials:                     # Specify the user IDs and passwords
            alpha: alpha                 # User: alpha has password: alpha
            beta: beta                   # Similarly for beta
        template: $YAMLPATH/login.html   # Optional login template
```
## log out
This configuration creates a `logout page`:
```
logout
    pattern: /$YAMLURL/logout   # Map this URL
    handler: LogoutHandler      # to the logout handler
    kwargs:
        redirect: /$YAMLURL/login/
```

Similiary you can have other login authentication like `google auth`, `facebook auth`, `twitter auth` etc..

# Start with ML application click [here](https://github.com/kamleshdjango/gramex-ml-workshop/blob/scipy-workshop/ml.md)
