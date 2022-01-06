from dataclasses import dataclass
from commiter.src.types import StatusEnum
from datetime import datetime
from commiter.src.utils import current_commit_hash, get_commit_date


@dataclass()
class Task1:
    description: str
    status: StatusEnum
    date: datetime = get_commit_date()
    commit: str = current_commit_hash()
    url_link: str = ''
    issue: int = -1
