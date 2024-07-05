from typing import List
from mirascope.anthropic import AnthropicCall, AnthropicCallParams


class Think(AnthropicCall):
    prompt_template = """
Make a prediction about what {name} is thinking based on the conversation history:
<conversation_history>
{history}
</conversation_history>
Use your Theory of Mind skills to make a prediction. If there isn't enough conversation history to make a prediction, just say "not enough conversation history yet".
"""
    name: str
    history: List[str]
    call_params = AnthropicCallParams(model="claude-3-5-sonnet-20240620")


class Converse(AnthropicCall):
    prompt_template = """
You're a conversational assistant. Craft a response to {name} based on the conversation history and context given:
<conversation_history>
{history}
</conversation_history>
<context>
{thought}
</context>
Keep your response brief, casual, and concise. Resist the urge to knowledge dump unless explicitly asked.
"""
    history: List[str]
    name: str
    thought: str
    call_params = AnthropicCallParams(model="claude-3-5-sonnet-20240620")

class Summarize(AnthropicCall):
    prompt_template = """
Summarize the conversation history:
<conversation_history>
{history}
</conversation_history>
"""
    history: List[str]
    call_params = AnthropicCallParams(model="claude-3-5-sonnet-20240620")
