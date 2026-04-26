from pathlib import Path
from .read_yaml import read_yaml

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(agent_name: str) -> dict:
    file_path = PROMPTS_DIR / f"{agent_name}_prompt.yaml"
    return read_yaml(str(file_path))
