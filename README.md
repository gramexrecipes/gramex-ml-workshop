Building a ML Classification application with Gramex
====================================

## Step 1 - Setup and Installation

To install gramex and its dependencies, please see the [installation guide](install.md).

## Step 2 - Overview

- Structure of workshop in [structure.md](structure.md).
- Workshop walkthrough instructions in [snippets/](snippets/) directory.

### Step 2.1 - Workshop Outline

The workshop content is prepared for 1.5 hrs.

| Section | Content | Duration |
| ------- | ------- | -------- |
| [Introduction](structure.md#introduction) | Gramex intro, controlling data with URL params | 20 mins|
| [Build an ML app](structure.md#snippets) | Use snippets and build the application step-by-step | 50 mins |
| Q&A, Support | Q&A session, help the participants | 10 mins |
| [Possibilities](structure.md#possibilities) | Other ML applications, Email alerts, Charts, Screenshots, Admin module | 10 mins |

### Step 2.2 - Overview of file structure

Files for building the application:

- `gramex.yaml`           - route configuration for endpoints
- `index.html`            - page that serves the application content
- `template-navbar.html`  - navbar content
- `style.css`             - `CSS` rules
- `report.html`           - classification output renderer

Files for the workshop:

- `structure.md` - workshop introduction
- `snippets`     - code snippets to build application
- `final.html`   - compare your final application against this

## Run locally

* To set up and use this application locally, see the [installation instructions](demo_setup.md).
* To learn how this app was built, see the [tutorial](tutorial.md)

# For workshop organizers

Please review the instructions on how this workshop content is put together: https://github.com/bkamapantula/gramex-ml-workshop/blob/master/demo_setup.md

## What to say

- How Gramex can help build custom applications
  - interactions
  - charts
- How to use Gramex to build ML as a service

In the workshop, participants will learn how to create API endpoints for data and ML services.

# For workshop participants

## Audience and prerequisites

The workshop is intended for developers who are new to Gramex.

### Prerequisites

- Participants are expected to be comfortable with programming (intro-level HTML, JavaScript, Python).

## Objective of the workshop

Participants will get familiar with few [Gramex](https://learn.gramener.com/guide/) components: back-end configuration via YAML, writing front-end (`JavaScript`) code.

## At the end of the workshop

Participants will get familiar with different utilities in Gramex to

- handle data (using [FormHandler](https://learn.gramener.com/guide/formhandler/))
- run arbitrary functions (using [FunctionHandler](https://learn.gramener.com/guide/formhandler/))
- customize components (using [UIComponents](https://learn.gramener.com/guide/uicomponents/))
  - add a utility to upload files (using [UploadHandler](https://learn.gramener.com/guide/uploadhandler/))
  - add an interactive table (using [g1 FormHandler](https://learn.gramener.com/guide/g1/formhandler))
  - productionize machine learning models
    - add endpoints to control machine learning classification algorithms in the UI
    - in the backend, explore how to use `scikit-learn` on-the-fly

# Contributors

Content for the workshops is prepared by below contributors:

- Jaidev Deshpande <jaidev.deshpande@gramener.com>
- Nivedita Deshmukh <nivedita.deshmukh@gramener.com>
- Kamlesh Jaiswal <kamlesh.jaiswal@gramener.com>
- Bhanu Kamapantula <bhanu.kamapantula@gramener.com>
