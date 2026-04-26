---
name: YAML-driven agent config
overview: Extract all hardcoded values from x_agent.py into x_agent_prompt.yaml, and build reusable read_yaml / prompt_loader utilities that follow a naming convention (agent_name -> agent_name_prompt.yaml) so future agents can load config the same way.
todos:
  - id: yaml-prompt
    content: Write x_agent_prompt.yaml with model, system_prompt, and tools fields
    status: completed
  - id: read-yaml
    content: Write read_yaml.py -- generic YAML file reader
    status: completed
  - id: prompt-loader
    content: Write prompt_loader.py -- convention-based loader using agent name
    status: completed
  - id: refactor-agent
    content: Refactor x_agent.py to load all config from YAML via prompt_loader
    status: completed
isProject: false
---

# YAML-Driven Agent Configuration

## Current State

[`src/agents/x_agent.py`](src/agents/x_agent.py) has these hardcoded values:
- `model = "openai:gpt-5.4-mini"`
- `system_prompt = "You are a helpful assistant..."`
- `tools = []`
- the user message `"Explain machine learning"`
- the `.env` path `"../../.env"`

## What Changes

### 1. `src/prompts/x_agent_prompt.yaml` -- agent config + prompt

Store all agent-level configuration here so behavior changes only require editing this file:

```yaml
model: "openai:gpt-5.4-mini"
system_prompt: |
  You are a helpful conversational assistant.
  You answer questions clearly and concisely.
  You can help with a wide range of tasks including
  explaining concepts, brainstorming ideas, and general Q&A.
tools: []
```

The `system_prompt` field drives the agent's personality and constraints. Future additions (temperature, max_tokens, tool configs, etc.) go here too -- no code changes needed.

### 2. `src/utils/read_yaml.py` -- generic YAML reader

A simple function that takes a file path, reads it, and returns the parsed dict:

```python
import yaml
from pathlib import Path

def read_yaml(file_path: str) -> dict:
    path = Path(file_path)
    with open(path, "r") as f:
        return yaml.safe_load(f)
```

### 3. `src/utils/prompt_loader.py` -- convention-based loader

Uses the naming convention `{agent_name} -> src/prompts/{agent_name}_prompt.yaml` to auto-resolve the YAML path:

```python
from pathlib import Path
from src.utils.read_yaml import read_yaml

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

def load_prompt(agent_name: str) -> dict:
    file_path = PROMPTS_DIR / f"{agent_name}_prompt.yaml"
    return read_yaml(str(file_path))
```

For any future agent (e.g. `research_agent`), just create `src/prompts/research_agent_prompt.yaml` and call `load_prompt("research_agent")`.

### 4. `src/agents/x_agent.py` -- simplified, config-driven

Replace hardcoded values with a `load_prompt("x_agent")` call:

```python
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from src.utils.prompt_loader import load_prompt

load_dotenv()

config = load_prompt("x_agent")

model = init_chat_model(model=config["model"])

agent = create_agent(
    model=model,
    tools=config.get("tools", []),
    system_prompt=config["system_prompt"],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": input("You: ")}]}
)

print(result["messages"][-1].content)
```

Key changes:
- No more hardcoded model, prompt, or tools -- all from YAML
- `load_dotenv()` without a relative path (it auto-finds `.env` from project root)
- `input("You: ")` replaces the hardcoded user message, enabling actual chat
- Minimal structure so adding features (streaming, memory, tools) later is easy

## File Summary

| File | Action |
|---|---|
| `src/prompts/x_agent_prompt.yaml` | Write config + system prompt |
| `src/utils/read_yaml.py` | Write generic YAML reader |
| `src/utils/prompt_loader.py` | Write convention-based loader |
| `src/agents/x_agent.py` | Refactor to use config |
