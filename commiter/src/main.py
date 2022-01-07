from commiter.src.factories import Processor, Factory1
from pathlib import Path


if __name__ == "__main__":
    command = "!a test"
    path_config = Path(__file__).parent.parent.joinpath(
        "data", "config.json").resolve()
    print(f"Using config file at : {path_config}")
    path_backup = path_config.parent.parent.joinpath("progress.json")
    task_type, backend, selector, actions = Factory1().create(
        path_config, path_backup)
    processor = Processor(backend, actions)
    processor.process(command)
