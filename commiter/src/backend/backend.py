from pathlib import Path
import json
from commiter.src.backend.tasks import Task1, AbstractTask
from typing import *
import pandas as pd


class Backend:
    def __init__(self, path: Path, tasks_parsers: Sequence[AbstractTask]):
        self.path = path
        self.tasks_parsers = tasks_parsers
        if not self.path.is_file():
            self.data = self.get_default_project_content()
            self.write()
        self.read()

    def get_default_project_content(self) -> dict:
        return {
            "project_properties": {},
            "tasks": [],
        }

    def read(self):
        with open(self.path) as fp:
            data = json.load(fp)

        self.data = data
        tasks = []
        for dico in data["tasks"]:
            parsed = False
            for parser in self.tasks_parsers:
                if parser.can_parse_dico(dico):
                    try:
                        tasks.append(parser.parse_dico(dico))
                        parsed = True
                    except Exception:
                        pass
                    break
            if not parsed:
                raise Exception(f"Unable to parse task {dico}")
        self.data["tasks"] = tasks

    def write(self):
        tasks = []
        for task in self.get_tasks():
            tasks.append(task.get_dico())
            self.data["tasks"] = tasks
        with open(self.path, "w") as fp:
            json.dump(self.data, fp)

    def get_tasks_dataframe(self):
        l_tasks_formatted = [t.get_dico() for t in self.get_tasks()]
        return pd.DataFrame(l_tasks_formatted)

    def from_tasks_dataframe(self, df: pd.DataFrame):
        for dico in df.to_dict('records'):
            parsed = False
            for task_parser in self.tasks_parsers:
                if task_parser.can_parse_dico(dico):
                    self.data["tasks"].append(task_parser.parse_dico(dico))
                    parsed = True
                    break
            if not parsed:
                print(
                    f"Cannot parse task {dico} with parsers {self.tasks_parsers}"
                )

    def add_task(self, tasks: Sequence[AbstractTask]):
        """:warning: This method add as it the objects (potential mutability problems)"""
        self.data["tasks"].extend(tasks)

    def delete_task(self, tasks: Sequence[int]):
        new_tasks = [t for i, t in enumerate(
            self.get_tasks()) if i not in tasks]
        self.data["tasks"] = new_tasks

    def get_tasks(self) -> List[AbstractTask]:
        return self.data["tasks"]
