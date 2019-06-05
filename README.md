# Overview

This document outlines the steps take to create this project. The idea is that it be used as a learning aid.

# Getting Started

Install the following tools:

    -   vscode (https://code.visualstudio.com/)
    -   Git Client (https://git-scm.com/downloads)
    -   Python 3.6+ (https://www.python.org/downloads/)
    -   Poetry (https://poetry.eustace.io/docs/#installation)
    -   Postman (https://www.getpostman.com/)

# Create Project

## Package Dependency Management

Install poetry to manage your package dependencies:

Create a new project:

```bash
mkdir ~/Documents/code
cd ~/Documents/code
poetry new templates-demo
```

## Create Git Repository

Initialize the project as a git repository:

```bash
cd ~/Documents/code/templates-demo
wget https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore -O .gitignore
```

Push up to the remote git repository:

```bash
git remote add origin git@ssh.dev.azure.com:v3/loudsquelch/templates-demo/templates-demo
git push -u origin --all
```

## Set up Virtual Environment

Create a virtual environment:

```bash
python3 -m venv ~/Documents/code/templates-demo/.venv
```

Activate the virtual environment:

```bash
. .venv/bin/activate
```

# Part 1: Script to Render Templates

## Add Dependencies

We will be using Jinja2 to render our templates. Use poetry to add the dependency to our project:

```bash
poetry add jinja2
```

Create _simple.md_ (a markdown template we can use for testing basic functionality):

```bash
mkdir ~/Documents/code/templates-demo/templates_demo/templates
touch ~/Documents/code/templates-demo/templates_demo/templates/simple.md
```

Create _render_template_ (a script to render ANY template, provided one or more variables to substitute in):

```bash
touch ~/Documents/code/templates-demo/templates_demo/render_template.py
```

Write the code...and then test...

```bash
~/Documents/code/templates-demo/templates_demo/render_template.py -variables "Hair Colour"=Jinja,"Template Engine"=Jinja2,Biscuit="Jinja Nut" --template simple.md --output-file /tmp/test.md
```

# Part 2: Ever Built a REST API?

We think this script is pretty useful so we are going to turn it in to a REST API...

## Add Dependencies

We will be using FastAPI (which will be running on an ASGI server called Uvicorn):

```bash
poetry add fastapi
poetry add uvicorn
```

## Bring up a Simple API

Create basic structure for the 'MVP' of our API:

```bash
mkdir ~/Documents/code/templates-demo/templates_demo/app
touch ~/Documents/code/templates-demo/templates_demo/app/__init__.py
touch ~/Documents/code/templates-demo/templates_demo/app/mvp.py
```

Write the code in main.py to create the application and add a single route that will return the API version:

```python
from fastapi import FastAPI

VERSION = "0.1.0"

app = FastAPI()

@app.get("/version")
async def read_version():
    return {"name:": "Templates Demo", "api_version": VERSION}
```

Run the application in the Uvicorn ASGI server (the '--reload' argument will case the server to auto-reload everytime a file is updated with new code):

```bash
cd ~/Documents/code/templates-demo/templates_demo/app
uvicorn mvp:app --reload
```

By default the server will run on port 8000. Hit http://localhost:8000/version with a web browser to get our API version number:

```json
{
  "name:": "Templates Demo",
  "api_version": "0.1.0"
}
```

> _NOTE_: Hitting an an invalid URL will return a 404 with a generic error message.

Now browse to http://localhost:8000/docs to see the auto-generated docs for our API!

Kill the application (using Ctrl+C) and now let's moving our template renderer in to the API...

# Part 3: Making our REST API useful!

What will it do?

1. Return its version number
2. Return all the templates it knows about
3. Accept new templates via an HTTP POST
4. Return a single template (known by id)
5. Render a template given a template id and a dictionary of variables supplied via an HTTP POST

## Create the API Paths

Create the entry point for our main application:

```bash
touch ~/Documents/code/templates-demo/templates_demo/app/main.py
```

The routers package:

```bash
mkdir ~/Documents/code/templates-demo/templates_demo/app/routers
touch ~/Documents/code/templates-demo/templates_demo/app/routers/__init__.py
touch ~/Documents/code/templates-demo/templates_demo/app/routers/templates.py
touch ~/Documents/code/templates-demo/templates_demo/app/routers/version.py
```

We can test our new application as follows:

```bash
cd ~/Documents/code/templates-demo/templates_demo/app
uvicorn main:app --reload
```

## Add Some Real functionality

Create a new module:

```bash
touch /home/craig/Documents/code/templates-demo/templates_demo/templates/library.py
```

It will need the following functionality:

- the ability to load existing templates from a folder
- save new templates to a folder
- remove a template
- render a template (with arbitrary variables that are provided by the user)

_T.B.A._

# Part 4: Shall we run it in Docker?

_T.B.A._

# Part 5: Eeek! What about logging?

_T.B.A._

# Part 6: Let's Add a Database Back-End

_T.B.A._
