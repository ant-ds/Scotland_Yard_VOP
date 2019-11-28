# VOP: Project - Gravensburger
This project originates from "Ingenieursproject II" in the bachelor of civil engineering at Ghent University, computer science.
It aims at making a computer opponent for the boardgame Ravensburger by use of a manually written algorithm, and a machine learning algorithm.

## Custom Settings and parameters

Some settings, like allowing for Multithreaded drawing, size of the window drawn, verbosity, ... should be kept user-specific and thus outside of
the git repository. Therefore you should run the code once, this will auto-generate a config file called *settings.ini*. Here you can keep all your desired settings for this project without having to change them for after every commit. An example default generated file can be seen below:

```ini
[DISPLAY]
multithreaded_drawing = true
display_mode = -1


[OUTPUT]
verbose = true
visualize = true
```

This file will be updated more in the future.

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

For running a 'data farm' you can run a script like the following

For Windows: 
```sh
#!/bin/sh
for i in {1..15000}
do
  pipenv run python scotlandyard.py
done
```

or for Unix systems:
```sh
#!/bin/bash
for i in $(eval echo {${1}..${2}..200})
do
   mkdir -p "history/manylayermodel$i"
   pipenv run python scotlandyard.py --proj "manylayermodel${i}/" --runs $3 --episodes $i


   mkdir -p "history/manylayermodel${i}VRandom"
   pipenv run python scotlandyard.py --proj "manylayermodel${i}VRandom/" --runs $3 --episodes $i --random y

   echo "Done with ${i} episodes!"
done
echo "Done"
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

## Integrating a custom AI

1. Create a class inheriting from the MisterX or Detective class, template:


```python
from game.misterx import MisterX


class ExampleAIImplementationMisterX(MisterX):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        return 153, 'taxi'
```

2. Add your custom class to the game instance. Game automatically generates its players, but allows you to overwrite them with two methods: *addMisterX* and *addDetectives*, which take your custom instances as arguments.

3. Run the game like any other game instance with your custom AI.

## Have fun developing :)
