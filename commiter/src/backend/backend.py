from pathlib import Path
import json


class Backend:
    def __init__(self, path: Path):
        self.path = path
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

    def flush(self):
        with open(self.path, "w") as fp:
            json.dump(self.data, fp)

    def add_task(self, task: dict):
        self.data["tasks"].append(task)
