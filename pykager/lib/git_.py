from pathlib import Path
from typing import Union, Optional

import git

from pykager.utils import cached_property


class Git:

    def __init__(self, directory: Union[str, Path]):
        self.__directory = directory

    @property
    def directory(self):
        return self.__directory

    @cached_property
    def repository(self) -> Optional[git.Repo]:
        try:
            return git.Repo(self.directory)
        except git.exc.InvalidGitRepositoryError:
            return

    @cached_property
    def commit(self) -> Optional[git.Commit]:
        if self.repository:
            return self.repository.head.commit

    @cached_property
    def author(self) -> Optional[git.Actor]:
        if self.commit and self.commit.author:
            return self.commit.author

    @cached_property
    def url(self) -> Optional[str]:
        if self.repository and len(self.repository.remotes) > 0:
            git_url = self.repository.remotes[0].config_reader.get("url")
            if git_url.endswith(".git"):
                git_url = git_url[:-4]
            return git_url


if __name__ == "__main__":
    g = Git(r"C:\Users\nathan\Desktop\Programming\python")
    print(g.commit)
