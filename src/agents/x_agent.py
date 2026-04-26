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
    {"messages": [{"role": "user", "content": input("You : ")}]}
)

print(result["messages"][-1].content)
