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

    @property
    def author_name(self):
        if self.author:
            return self.author.name

    @property
    def author_email(self):
        if self.author:
            return self.author.email

    @cached_property
    def url(self) -> Optional[str]:
        if self.repository and len(self.repository.remotes) > 0:
            git_url = self.repository.remotes[0].config_reader.get("url")
            if git_url.endswith(".git"):
                git_url = git_url[:-4]
            return git_url

    @cached_property
    def name(self) -> Optional[str]:
        if self.url:
            return self.url.split("/")[-1]


if __name__ == "__main__":
    g = Git(r"C:\Users\nathan\Desktop\Programming\python\Important Misc\imperial-py")
    print(g.url)
