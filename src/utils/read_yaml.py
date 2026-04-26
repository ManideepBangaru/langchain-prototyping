import yaml
from pathlib import Path


def read_yaml(file_path: str) -> dict:
    path = Path(file_path)
    with open(path, "r") as f:
        return yaml.safe_load(f)
