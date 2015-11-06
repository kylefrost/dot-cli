# dot

Easily manage dotfiles through the command line.

# Prerequisites

- `git` set up on your machine.
    - Must use SSH key authentication. For more infomrmatin see [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys/).
    - *You already should be doing this for security purposes, anyway.*
- A GitHub repo to store your dotfiles (default repo name is `dotfiles`).
    - [Create a repo](https://github.com/new), named anything you want. It can even be private!
        - *If it is private, you must make sure to be using SSH key authentication, otherwise dot won't have permission to push*
- `pip` (Python package manager)

# Installation

Simply run:

    $ pip install dot
    
Or if you want to install it from source
    
    $ git clone https://github.com/kylefrost/dot.git
    $ cd dot/
    $ python setup.py install


# Usage

Initial Setup:

    $ dot config

This will ask for your GitHub username and the name of the repo which you wish to store your dotfiles.

Add dotfiles to be tracked:

    $ dot track [file]

Must include the beginning `.`.

Push dotfiles to GitHub:

    $ dot push

Pull dotfiles from GitHub:

    $ dot pull

Manually update options:

    $ dot config [option] [value]

Or, update the file located at `$HOME/.dotconfig`.

# Notes

The only thing `dot` stores in regards to your `git` information is your username and your dotfiles repository name. I never ask for your password or your SSH keys. You can see all of the logic for interacting with git in [`dot/git.py`](dot/git.py). `git` runs as the current user when you use `dot`, this is why SSH key authentication is a [prerequisite](https://github.com/kylefrost/dot#prerequisites), to make things go smoother.

# License

[GNU GPL v3.0](LICENSE)
