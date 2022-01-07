from commiter.src.backend.backend import Backend
from pathlib import Path
from commiter.src.command.actions import *
from commiter.src.command.selectors import *
from commiter.src.backend.tasks import *


class Factory1:
    def create(self, path_config: Path, path_backup: Path):
        task_type = Task1
        backend = Backend(path=path_backup, tasks_parsers=[task_type])
        selector = IndexSelector(backend)
        actions = [AddTask(backend, task_type), DeleteTask(backend, selector), ModifyProperty(
            backend, selector), Issue(backend, task_type, selector)]
        return task_type, backend, selector, actions


class Processor:
    def __init__(self, backend: Backend, actions: List):
        self.backend = backend
        self.actions = actions

    def process(self, command: str):
        commands = command.split(";")
        for command in commands:
            for action in self.actions:
                if action.can_parse(command):
                    action.parse(command)
                    break
            else:
                print("Unknown command: " + command)
        self.backend.write()
