# VOP: Project - Gravensburger

## Building
### Installing pipenv

Using pip:
```sh
$ pip install --user pipenv
```

Using Homebrew (Mac):
```sh
$ brew install pipenv
```

### Installing pyenv (not sure if this works in windows)

This will get you going with the latest version of pyenv and make it
easy to fork and contribute any changes back upstream.

1. **Check out pyenv where you want it installed.**
   A good place to choose is `$HOME/.pyenv` (but you can install it somewhere else).

        $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv


2. **Define environment variable `PYENV_ROOT`** to point to the path where
   pyenv repo is cloned and add `$PYENV_ROOT/bin` to your `$PATH` for access
   to the `pyenv` command-line utility.

    ```sh
    $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    ```
    **Zsh note**: Modify your `~/.zshenv` file instead of `~/.bash_profile`.
    **Ubuntu and Fedora note**: Modify your `~/.bashrc` file instead of `~/.bash_profile`.
    **Proxy note**: If you use a proxy, export `http_proxy` and `HTTPS_PROXY` too.

3. **Add `pyenv init` to your shell** to enable shims and autocompletion.
   Please make sure `eval "$(pyenv init -)"` is placed toward the end of the shell
   configuration file since it manipulates `PATH` during the initialization.
    ```sh
    $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
    ```
    - **Zsh note**: Modify your `~/.zshenv` file instead of `~/.bash_profile`.
    - **fish note**: Use `pyenv init - | source` instead of `eval (pyenv init -)`.
    - **Ubuntu and Fedora note**: Modify your `~/.bashrc` file instead of `~/.bash_profile`.

    **General warning**: There are some systems where the `sh_ENV` variable is configured
    to point to `.bashrc`. On such systems you should almost certainly put the abovementioned line
    `eval "$(pyenv init -)"` into `.bash_profile`, and **not** into `.bashrc`. Otherwise you
    may observe strange behaviour, such as `pyenv` getting into an infinite loop.
    See [#264](https://github.com/pyenv/pyenv/issues/264) for details.

4. **Restart your shell so the path changes take effect.**
   You can now begin using pyenv.
    ```sh
    $ exec "$SHELL"
    ```


### Installing requirements

To install all dependencies listed in the Pipfile:
```sh
$ pipenv install
```

If you are a developer who cares about styling, flake8 is part of the 'dev' packages. To install dev packages as well do:
```sh
$ pipenv install --dev
```
(see below for a flake8 for vscode setup)

It it possible to run into an error like:

```python
TypeError: 'module' object is not callable
```

This is (usually) related to a newer pip version not being compatible with operations performed, a suggestion is to run

```sh
$ pipenv run pip install pip==18.0
```


### Running code

To run code for project-gravensburger, use commands you are familiar with, prefixed with "pipenv run". So a run of the current implementation of the game Scotland Yard would be:

```sh
$ pipenv run python scotlandyard.py
```

## Testing and development

### Styling

To adhere to a consistent styling in the code we will use the flake8 linter for python. It is included with a simple variation of the default install command:

```sh
$ pipenv install --dev
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