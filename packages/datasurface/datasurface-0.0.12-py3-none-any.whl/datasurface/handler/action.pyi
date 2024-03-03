from datasurface.md.GitOps import GitHubRepository as GitHubRepository, Repository as Repository
from datasurface.md.Governance import Ecosystem as Ecosystem
from datasurface.md.Lint import ValidationTree as ValidationTree
from typing import Optional

def getEcosystem(path: str) -> Optional[Ecosystem]: ...
def verifyPullRequest() -> ValidationTree: ...
