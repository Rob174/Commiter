from abc import ABC, abstractmethod
import re
from commiter.src.types import Status
from commiter.src.utils import parse_printer_format_range
from commiter.src.command.observers import *
from commiter.src.backend.tasks import AbstractTask
from commiter.src.command.selectors import *


class AbstractAction(TaskObservable):
    def __init__(self, backend: Backend, callbacks: List[AbstractTaskCallback] = None):
        super(AbstractAction, self).__init__(callbacks)
        self.backend = backend

    @abstractmethod
    def can_parse(self, string: str) -> bool:
        pass

    @abstractmethod
    def parse(self, string: str):
        pass

    @abstractmethod
    def perform(self, *args, **kwargs):
        pass


class AddTask(AbstractAction):
    def __init__(self, backend: Backend, task_class, callbacks: List[AbstractTaskCallback] = None):
        super(AddTask, self).__init__(backend, callbacks)
        self.global_regex = r"^!a (.+)"
        self.task_class = task_class

    def can_parse(self, string: str) -> bool:
        return re.match(self.global_regex, string) is not None

    def parse(self, string: str):
        tasks_descr = re.match(self.global_regex, string).group(1).split("!,")
        self.on_before_action()
        tasks = []
        for t_d in tasks_descr:
            tasks.append(self.task_class.parse_string(t_d))
        self.backend.add_task(tasks)
        self.on_after_action()


class DeleteTask(AbstractAction):
    def __init__(self, backend: Backend, selector: AbstractSelector, callbacks: List[AbstractTaskCallback] = None):
        super(DeleteTask, self).__init__(backend, callbacks)
        self.selector = selector
        self.global_regex = r"^!d (.*)"

    def can_parse(self, string: str) -> bool:
        match = re.match(self.global_regex, string)
        if match is not None:
            return self.selector.can_use(match.group(1))
        else:
            return False

    def parse(self, string: str):
        range_str = re.match(self.global_regex, string).group(1)
        self.on_before_action()
        selection = [i for i in self.selector.parse(range_str)]
        for i in selection:
            self.backend.delete_task(i)
        self.on_after_action()


class ModifyProperty(AbstractAction):
    def __init__(self, backend: Backend, selector: AbstractSelector, callbacks: List[AbstractTaskCallback] = None):
        super(ModifyProperty, self).__init__(backend, callbacks)
        self.global_regex = r"^!m_([A-Za-z.0-9]+) (.*) (.*)"

    def can_parse(self, string: str) -> bool:
        match = self.match(self.global_regex, string)
        if match is None:
            return False
        return self.selector.can_use(match.group(2))

    def parse(self, string: str):
        match = self.match(self.global_regex, string)
        tasks = self.selector.parse(match.group(2))
        for t in tasks:
            t.modify(match.group(1), match.group(3))


class Issue(AbstractAction):
    def __init__(self, backend: Backend, task_class: AbstractTask, selector: AbstractSelector, callbacks: List[AbstractTaskCallback] = None):
        super(Issue, self).__init__(backend, callbacks)
        self.task_class = task_class
        self.global_regex = r"^!bug (.*)"
        self.selector = selector

    def can_parse(self, string: str) -> bool:
        match = self.match(self.global_regex, string)
        return match is None

    def parse(self, string: str):
        match = re.match(self.global_regex, string)
        content = match.group(1)
        # if nothing specified, we assume that evreything is bugged
        if content == "":
            for t in self.backend.get_tasks():
                t.set_status(self.task_class.get_bugged_status())
            return
        # else a selector is expected to specify potentially affected functionnalities
        if not self.selector.can_use(content):
            raise Exception(f"Malformatted selector {content} in {string}")
        for t in self.selector.select(content):
            t.set_status(self.task_class.get_bugged_status())
