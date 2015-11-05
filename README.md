# dot

Easily manage dotfiles through the command line.

# Prerequisites

- `git` set up on your machine.
    - Must use SSH key authentication. For more infomrmatin see [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys/).
- A GitHub repo to store your dotfiles (default repo name is `dotfiles`).
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

# License

[GNU GPL v3.0](LICENSE)
