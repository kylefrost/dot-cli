import os
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
            gclone = subprocess.call(["git", "clone", git_url, "."], stdout=fnull, stderr=subprocess.STDOUT)

            with open("README.md", 'a+') as readme:
                readme.write("\n\n### Managed by [dot](https://github.com/kylefrost/dot)")

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
