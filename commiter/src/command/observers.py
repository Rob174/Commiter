from typing import *
from abc import ABC, abstractmethod
from commiter.src.backend.backend import Backend


class AbstractTaskCallback(ABC):
    def before_action(self):
        pass

    def after_action(self):
        pass


class AbstractCommitFormatter(ABC):
    def __init__(self, backend: Backend):
        self.backend = backend

    @abstractmethod
    def format(self) -> str:
        pass


class CommitCallback(AbstractTaskCallback):
    def __init__(self, commit_formatter: AbstractCommitFormatter, extensions: Optional[Sequence[str]] = None):
        if extensions is None:
            extensions = [".py"]
        self.extensions = [f":/*{extension}" for extension in extensions]
        self.commit_formatter = commit_formatter

    def on_after_action(self):
        subprocess.check_call(["git", "add", *self.extensions])
        subprocess.check_call(
            ["git", "commit", "-m", self.commit_formatter.format()]
        )


class TaskObservable:
    def __init__(self, callbacks: List[AbstractTaskCallback] = None):
        self.callbacks = callbacks if callbacks is not None else []

    def on_before_action(self):
        for c in self.callbacks:
            c.before_action()

    def on_after_action(self):
        for c in self.callbacks:
            c.after_action()
