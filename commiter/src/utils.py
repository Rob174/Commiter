from typing import Optional
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


def get_commit_date(previous: Optional[int] = None) -> datetime:
    date_str = subprocess.check_output(
        ['git', 'log',
            'HEAD' if previous is None else f'HEAD~{previous}', "--format=%cd", "--date=local"]
    ).decode('utf-8').strip()
    return parser.parse(date_str)
