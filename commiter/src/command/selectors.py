from abc import ABC, abstractmethod
from commiter.src.backend.backend import Backend
from commiter.src.utils import parse_printer_format_range


class AbstractSelector(ABC):
    def __init__(self, backend: Backend):
        self.backend = backend

    @abstractmethod
    def can_use(self, string: str) -> bool:
        pass

    @abstractmethod
    def select(self, *args, **kwargs) -> dict:
        pass


class IndexSelector(AbstractSelector):
    def __init__(self, backend: Backend):
        super().__init__(backend)
        self.global_regex = r"^(((\d+-\d+|\d),)*(\d+-\d+|\d))"

    def can_use(self, string: str) -> bool:
        return re.match(self.global_regex, string) is not None

    def select(self, string: str) -> dict:
        indexes = parse_printer_format_range(string)
        new_tasks = {i: t for i, t in enumerate(
            self.backend.get_tasks()) if i in indexes
        }
        return new_tasks


class DFSelector(AbstractSelector):
    def __init__(self, backend: Backend):
        super().__init__(backend)

    def can_use(self, string: str) -> bool:
        df = self.backend.get_tasks_dataframe()
        try:
            df.query(string)
            return True
        except Exception:
            return False

    def select(self, string: str) -> dict:
        df = self.backend.get_tasks_dataframe()
        df = df.query(string)
        return {int(re.match(r"row(\d+)", k).group(1)): v for k, v in df.to_dict('index').items()}
