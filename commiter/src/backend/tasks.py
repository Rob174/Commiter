from dataclasses import dataclass
from commiter.src.types import StatusEnum
from datetime import datetime
from commiter.src.utils import current_commit_hash, get_commit_date, parse_commit_date
from abc import ABC


class AbstractTask(ABC):
    @staticmethod
    def parse(dico: dict) -> Task1:
        raise NotImplementedError

    def write(self) -> dict:
        raise NotImplementedError
    
    def can_parse(self,dico:dict):
        raise NotImplementedError


@dataclasses
class Task1(AbstractTask):
    description: str
    status: StatusEnum
    date: datetime = get_commit_date()
    commit: str = current_commit_hash()
    url_link: str = ''
    issue: int = -1

    @staticmethod
    def parse(dico: dict) -> Task1:
        return Task1(
            description=dico['description'],
            status=StatusEnum[dico['status']],
            date=parse_commit_date(dico["date"]),
            commit=dico['commit'],
            url_link=dico['url_link']
            issue=int(dico['issue'])
        )

    def write(self) -> dict:
        return {
            "description": self.description,
            "status": str(self.status),
            "date": self.date.strftime("%a %b %d %H:%M:%S %Y"),
            "commit": self.commit,
            "url_link": self.url_link,
            "issue": str(self.issue)
        }
    
    def can_parse(self,dico: dict) -> bool:
        keys = set(dico.keys())
        reference_keys = set({"description", "status", "date", "commit", "url_link", "issue"})
        return keys == reference_keys
