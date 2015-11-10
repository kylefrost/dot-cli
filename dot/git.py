import os
import click
import subprocess
from time import strftime

class Git:
    """Git Functionality for Dot"""
    
    _dotdir = "/.dot/"
    _github = "git@github.com:"

    def __init__(self, home, gitname, reponame):
        """Initializer for Git class object"""
        self.home = home
        self.gitname = gitname
        self.reponame = reponame
    
    def clone(self):
        """Git clone functionality"""
        dest_path = self.home + self._dotdir
        git_url = self._github + self.gitname + "/" + self.reponame + ".git"
        os.chdir(dest_path)
        with open(os.devnull, 'w') as fnull:
            gclone = subprocess.call(["git", "clone", git_url, "."], stdout=fnull, stderr=fnull)

        already_has_managed_text = False
        managed_text = "### Managed by [dot](https://github.com/kylefrost/dot)"

        if os.path.exists('README.md'):
            with open('README.md', 'r') as f:
                for line in f:
                    if "Managed by [dot]" in line:
                        already_has_managed_text = True

            with open('README.md', 'a+') as readme:
                if not already_has_managed_text:
                    readme.write("\n\n" + managed_text)
        else:
            click.secho("No README.md file found in repo.", fg='yellow')

        return gclone

    def pull(self):
        """Git pull functionality"""
        dest_path = self.home + self._dotdir
        os.chdir(dest_path)
        with open(os.devnull, 'w+') as fnull:
            gpull = subprocess.call(["git", "pull"], stdout=fnull, stderr=fnull)

        return gpull

    def push(self):
        """Git push functionality"""
        path = self.home + self._dotdir
        commit_msg = "dot: Updated dotfiles at " + strftime("%I:%M:%S %p") + " on " + strftime("%b %d")
        os.chdir(path)
        with open(os.devnull, 'w+') as fnull:
            add = subprocess.call(["git", "add", "--all"], stdout=fnull, stderr=fnull)
            commit = subprocess.call(["git", "commit", "-m", commit_msg], stdout=fnull, stderr=fnull)
            gpush = subprocess.call(["git", "push", "origin", "master"], stdout=fnull, stderr=fnull)

        return [add, commit, gpush]
