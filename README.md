# dot

Lightweight tool for managing dotfiles with git and the command line.

# Prerequisites

- `git` set up on your machine.
    - Must use SSH key authentication. For more information see [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys/).
        - *You really should be doing this for security purposes, anyway.*
- A GitHub repo to store your dotfiles (default repo name is `dotfiles`, setup during config), with a `README.md` file.
    - [Create a repo](https://github.com/new), named anything you want. It can even be private!
        - *If it is private, you must make sure to be using SSH key authentication, otherwise `dot` won't have permission to push.*
- [`pip`](https://pypi.python.org/pypi/pip) (Python package manager)

# Installation

Simply run:

    $ pip install dot
    
Or if you want the most up-to-date version (could be broken!):
    
    $ git clone https://github.com/kylefrost/dot.git
    $ cd dot/
    $ pip install -r requirements.txt
    $ python setup.py install


# Usage

### Initial Setup

This will ask for your GitHub username and the name of the repo which you wish to store your dotfiles.

    $ dot init


### Track dotfiles

Must include the beginning "`.`" if the file is hidden (which if it isn't, is it even a dotfile?).

    $ dot track [filename]


### Push dotfiles to repo

    $ dot push

### Pull dotfiles from repo

    $ dot pull

### Update `dot` options

*Alternatively, you can edit the file located at `$HOME/.dotconfig`.*

    $ dot config [option] [value]


# Notes

The only thing `dot` stores in regards to your `git` information is your username and your dotfiles repository name. I never ask for your password or your SSH keys. You can see all of the logic for interacting with `git` in [`dot/git.py`](dot/git.py). `git` runs as the current user when you use `dot`, this is why SSH key authentication is a [prerequisite](https://github.com/kylefrost/dot#prerequisites), to make things go smoother.

# Contribute

__Want a certain feature?__ [Open an issue](https://github.com/kylefrost/dot/issues) and label it `feature request`.

__Know how to code?__ [Open an issue](https://github.com/kylefrost/dot/issues) (if there isn't one), label it `in progress`, [fork this repo](https://github.com/kylefrost/dot/fork) and submit a [pull request](https://github.com/kylefrost/dot/pulls). If the issue already exists, add the `in progress` label to the existing issue (we don't need redundant issues!).

### Syntax and Comments

If you wish to contribute by editing or adding to the codebase, please follow the structure that is already in place (outlined briefly below).

- String comments as first line under function definitions
- Little to no comments, your code should speak for itself
    - If you write something that requires explaining, keep comments to-the-point
- Add appropriate `VerboseLog(message, ctx)` calls
- Use provided `GetConfig(section)` when reading `.dotconfig` file in [`cli.py`](dot/cli.py)
- Unused code should be removed, not left and commented out

# License

[GNU GPL v3.0](LICENSE)
