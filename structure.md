
# Building ML applications with Gramex

## What we will do today

- construct a simple app with building blocks (HTML, JS, python)
- create an app that trains and tests datasets and review the output

## What it needs

Make sure you install the [necessary software](prerequisites.md) before you arrive at the workshop.

Read: [prerequisites.md](prerequisites.md)

## Outline

The workshop begins at 11:30 am.

| Section | Content | Duration |
| ------- | ------- | -------- |
| [Introduction](#introduction) | Gramex intro, controlling data with URL params | 20 mins, 11:30 to 11:50 am |
| [Build an ML app](#ml-application) | Content | 20 mins, 11:31 to 11:51 am |
| What else | Email alerts, Charts, Screenshots, Admin module | 10 mins |

# Introduction

Gramex is a web and data server. One can do the below with minimal setup

- fetch, edit, delete data records
- execute arbitrary python
- auth support: database-based, active directory-based, google, social (twitter, facebook)
- capture screenshots
- configure smart email alerts

most of it via `YAML` configuration.

## URLs

Consider a dataset that you'd like to explore for exploratory data analysis.

Before that you'd like to see the composition of the file. You can expose it using `FormHandler`

```YAML
url:
  data-endpoint:
    pattern: /$YAMLURL/data
    handler: FormHandler
    kwargs:
      url: $YAMLPATH/iris.csv
      default:
        _limit: 5
```

Most handlers support `kwargs` section to control data from server-side.

Note that we've limited the number of rows to `5` irrespective of how many rows end user requests.

```
formats: JSON, CSV, HTML
```

### URL sections
Multiple URL sections can be 

### Arbitrary python
Arbitrary `python` code can be run using `FunctionHandler`.

```YAML
url:
  custom-python-code:
    pattern: /$YAMLURL/code
    handler: FunctionHandler
    kwargs:
      function: app.my_func
```

1. Access URL parameters via attributes

2. Return values


### Other Handlers, services

Gramex is built on top of `tornado` which uses `RequestHandler` for everything and we've sub-classed to different utilities for ease of use.

- `FileHandler`
- `CaptureHandler`
- `Scheduler`

# Snippets

Head to [snippets](snippets) directory to begin the application building.
