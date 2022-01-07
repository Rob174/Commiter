from dataclasses import dataclass, field, fields
from commiter.src.types import Status
from datetime import datetime
import dateutil
from commiter.src.utils import current_commit_hash, get_commit_date, parse_commit_date
from abc import ABC
from typing import *
from pathlib import Path
import re


class AbstractTask(ABC):

    def get_dico(self) -> dict:
        raise NotImplementedError

    def can_parse_dico(self, dico: dict):
        raise NotImplementedError

    def set_status(self, status: str):
        pass

    @staticmethod
    def get_bugged_status(self) -> str:
        with open(Path(__file__).parent.parent.joinpath("data", "config.json")) as fp:
            dico = json.load(fp)
        return dico["status.bug"]


@dataclass
class Task1(AbstractTask):
    description: str
    status: List[str] = field(default_factory=[])
    date: datetime = get_commit_date()
    commit: str = current_commit_hash()
    issue: List = field(default_factory=[])

    @staticmethod
    def parse_dico(dico: dict) -> 'Task1':
        return Task1(
            description=dico['description'],
            status=[Status.get(s)["default"] for s in dico['status']],
            date=parse_commit_date(dico["date"]),
            commit=dico['commit'],
            issue=[int(i) for i in dico['issue']]
        )

    def get_dico(self) -> dict:
        return {
            "description": self.description,
            "status": self.status,
            "date": self.date.strftime("%a %b %d %H:%M:%S %Y"),
            "commit": self.commit,
            "issue": [str(i) for i in self.issue]
        }

    @staticmethod
    def can_parse_dico(dico: dict) -> bool:
        keys = set(dico.keys())
        reference_keys = set(
            {"description", "status", "date", "commit", "issue"})
        return keys == reference_keys

    def set_status(self, status: str):
        status = Task1.parse_status(status)
        if status not in ["BUG"]:
            self.status.append(status)
        else:
            self.status = [status]

    @staticmethod
    def parse_string(string: str) -> 'Task1':
        match_issue = re.findall("#([0-9]+)", string)
        issues = []
        if match_issue is not None:
            issues = [int(i) for i in match_issue]
        match_status = re.match(f"!s (.*) ", string)
        if match_status is not None:
            status = [Task1.parse_status(match_status.group(1))]
        else:
            status = [Status.get_default_status()["default"]]
        abbr_possible = Status.get_iterable("abbreviation")
        return Task1(description=string, issue=issues, status=status)

    @staticmethod
    def parse_status(string: str) -> str:
        match_status = re.match(f"({'|'.join(abbr_possible)})", string)
        if match_status is not None:
            abbr = match_status.group(1)
            status = Status.get(abbr, specific_dict="abbreviation")
        else:
            status = Status.get_default_status()
        return status["default"]

    def modify(self, field: str, operation: str):
        def status_fn(x): return self.set_status(Task1.parse_status(x))
        dico_mapping = {
            "de": ("description",),
            "s": ("status", status_fn),
            "da": ("date", lambda x: dateutil.parser.parse(x)),
            "c": ("commit", ),
            "i": ("issue", lambda x: int(x))
        }
        if field not in dico_mapping:
            raise ValueError(f"{field} not in dico_mapping")
        if len(dico_mapping[field]) == 1:
            eval(dico_mapping[field][0]+" = "+operation)
        else:
            eval(dico_mapping[field][0]+" = dico_mapping[field][1](operation)")
