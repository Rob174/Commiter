from typing import *
import subprocess
from dateutil import parser
from datetime import datetime


def current_commit_hash(previous: Optional[int] = None) -> str:
    return subprocess.check_output(
        ['git', 'rev-parse',
                'HEAD' if previous is None else f'HEAD~{previous}']
    ).decode('utf-8').strip()


def get_short_hash(long_hash: str):
    return long_hash[:8]


def parse_commit_date(date: str) -> datetime:
    return datetime.strptime(date, "%a %b %d %H:%M:%S %Y")


def get_commit_date(previous: Optional[int] = None) -> datetime:
    commit_ref = "HEAD" if previous is None else f"HEAD~{previous}"
    date_str = subprocess.check_output(
        ['git', 'log', commit_ref, "--format=%cd", "--date=local"]
    ).decode('utf-8').strip().split("\n")[0]

    return parse_commit_date(date_str)


def parse_printer_format_range(string: str) -> Sequence[int]:
    string = string.split(",")  # type: ignore
    values = []
    for s in string:
        try:
            value = int(s)
            value = [value]
        except ValueError:
            value = s.split("-")
            value = list(range(int(value[0]), int(value[1])+1))
        values.extend(value)
    return values
