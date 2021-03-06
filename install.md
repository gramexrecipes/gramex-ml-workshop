Installation
============

In order to install gramex and other material required for the workshop, please follow the following instructions.

For most updated instructions, visit [https://gramener.com/gramex/guide/install/](https://gramener.com/gramex/guide/install/)

# Cloud installation

## Visit Gramex IDE website

Gramex IDE allows you to clone existing repositories or create new ones. Link: https://gramex.gramener.com/

Authenticate using GitHub.

## Clone this repository

Clone this workshop [repository](https://github.com/gramexrecipes/gramex-ml-workshop/) by pasting the link in the text box.

![clone repository URL](assets/ide-clone-repo.png)

## View details

View details of the cloned repository on the right side.

![cloned repository](assets/ide-cloned.png)

You can edit the content using the IDE in browser or initialize the application or view the logs.

# Local installation

## If you have anaconda

```bash
conda create -y --name gramex python=3.7            # Create a new environment
conda activate gramex                               # Activate it
conda install -y -c conda-forge -c gramener gramex  # Install Gramex
```

## If you don't have anaconda, use pip

Install [Anaconda3-2020.02](https://repo.anaconda.com/archive/). (Gramex does not yet work with Python 3.8. So avoid later versions). Here are downloads for:

 - [Windows-x86_64](https://repo.anaconda.com/archive/Anaconda3-2020.02-Windows-x86_64.exe)
 - [Windows-x86](https://repo.anaconda.com/archive/Anaconda2-2019.10-Windows-x86.exe)
 - [MacOSX-x86_64](https://repo.anaconda.com/archive/Anaconda2-2019.10-MacOSX-x86_64.pkg)
 - [Linux-x86_64](https://repo.anaconda.com/archive/Anaconda2-2019.10-Linux-x86_64.sh)
 - [Linux-ppc64le](https://repo.anaconda.com/archive/Anaconda2-2019.10-Linux-ppc64le.sh)

Then install [node.js](https://nodejs.org/en/) 10 or later:

```bash
pip install gramex      # Install latest version of Gramex
npm install -g yarn     # Required for UI components and built-in apps
gramex setup --all      # Set up UI components and built-in apps
```

You could also install Gramex via [docker](https://learn.gramener.com/guide/install/#docker-install) or in [offline](https://learn.gramener.com/guide/install/#offline-install) mode.

In case of any problems or questions, send an email to `cto@gramener.com`; or raise an issue [here](https://github.com/gramener/gramex/issues).
