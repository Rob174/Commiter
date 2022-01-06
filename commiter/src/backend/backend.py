from pathlib import Path
import json
from commiter.src.tasks.Task1 import Task1, AbstractTask
from typing import Sequence


class Backend:
    def __init__(self, path: Path, tasks_parsers: Sequence[AbstractTask]):
        self.path = path
        self.tasks_parsers = tasks_parsers
        if not self.path.is_file():
            self.data = self.get_default_project_content()
            self.flush()
        with open(self.path) as fp:
            self.data = json.load(fp)

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
                if parser.can_parse(dico):
                    try:
                        tasks.append(parser.parse(dico))
                    except Exception:
                        pass
                    break
            if not parsed:
                raise Exception(f"Unable to parse task {dico}")
        self.data["tasks"] = tasks

    def write(self):
        tasks = []
        for task in self.data["tasks"]:
            tasks.append(task.write())
            self.data["tasks"] = tasks
        with open(self.path, "w") as fp:
            json.dump(self.data, fp)

    def add_task(self, task: dict):
        self.data["tasks"].append(task)
