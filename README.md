# dot

Easily manage dotfiles through the command line.

# Prerequisites

- `git` set up on your machine.
    - Must use SSH key authentication. For more infomrmatin see [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys/).
        - *You already should be doing this for security purposes, anyway.*
- A GitHub repo to store your dotfiles (default repo name is `dotfiles`).
    - [Create a repo](https://github.com/new), named anything you want. It can even be private!
        - *If it is private, you must make sure to be using SSH key authentication, otherwise `dot` won't have permission to push.*
- `pip` (Python package manager)

# Installation

Simply run:

    $ pip install dot
    
Or if you want the most up-to-date version (could be broken!):
    
    $ git clone https://github.com/kylefrost/dot.git
    $ cd dot/
    $ python setup.py install


# Usage

### Initial Setup

This will ask for your GitHub username and the name of the repo which you wish to store your dotfiles.

    $ dot config


### Track dotfiles

Must include the beginning "`.`" if the file is hidden (which if it isn't, is it even a dotfile?).

    $ dot track [file]


### Push dotfiles to repo

    $ dot push

### Pull dotfiles to repo

    $ dot pull

### Update `dot` options

Alternatively, you can edit the file located at `$HOME/.dotconfig`.

    $ dot config [option] [value]


# Notes

The only thing `dot` stores in regards to your `git` information is your username and your dotfiles repository name. I never ask for your password or your SSH keys. You can see all of the logic for interacting with `git` in [`dot/git.py`](dot/git.py). `git` runs as the current user when you use `dot`, this is why SSH key authentication is a [prerequisite](https://github.com/kylefrost/dot#prerequisites), to make things go smoother.

# Contribute

#### Contributions are encouraged!

__Want a certain feature?__ [Open an issue](https://github.com/kylefrost/dot/issues) and label it `feature request`.

__Know how to code?__ [Fork this repo](https://github.com/kylefrost/dot/fork) and submit a [pull request](https://github.com/kylefrost/dot/pulls).

# License

[GNU GPL v3.0](LICENSE)
