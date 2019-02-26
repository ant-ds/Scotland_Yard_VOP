# VOP: Project - Gravensburger

## Building
### 1. Installing pipenv

Using pip:
```bash
pip install --user pipenv
```

Using Homebrew (Mac):
```bash
brew install pipenv
```


### 2. Installing requirements

To install all dependencies listed in the Pipfile:
```bash
pipenv install
```

If you are a developer who cares about styling, flake8 is part of the 'dev' packages. To install dev packages as well do:
```bash
pipenv install --dev
```
(see below for a flake8 for vscode setup)

### 3. Running code

To run code for project-gravensburger, use commands you are familiar with, prefixed with "pipenv run". So a run of the current implementation of the game Scotland Yard would be:

```bash
pipenv run python scotlandyard.py
```

## Testing and development

### Styling

To adhere to a consistent styling in the code we will use the flake8 linter for python. It is included with a simple variation of the default install command:

```bash
pipenv install --dev
```

Sadly some of the default parameters for flake8 include a max line length of about 90 characters, which is unbearably small. Therefore you should place a file called .flake8 in the directory also containing your Pipfile with contents:

```
[flake8]
max-line-length = 160
ignore=W293, W391, W291
```

This guarantees some of the more annoying warnings by flake8 will be ignored such as trailing whitespace. This file is local-only, so feel free to change its contents as long as it doesn't interfere with other developers.

### Testing and local files
Our .gitignore allows you to have certain local files inside the project-gravensburger directory: test.py and notes.txt. You can freely use files with these names to keep track of notes or circumstances during development or to run a testversion of your code.

## Have fun developing :)