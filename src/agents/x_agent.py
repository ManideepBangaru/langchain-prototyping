from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from src.utils.prompt_loader import load_prompt
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

# Load environment variables
load_dotenv()

# Load agent configuration
config = load_prompt("x_agent")

# Initialize models
basic_model = init_chat_model(model=config["basic_model"])
advance_model = init_chat_model(model=config["advance_model"])

# Dynamic model selection middleware
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advance_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,
    tools=config.get("tools", []),
    system_prompt=config["system_prompt"],
    middleware=[dynamic_model_selection],
) 

result = agent.invoke(
    {"messages": [{"role": "user", "content": input("You : ")}]}
)

print(result["messages"][-1].content)