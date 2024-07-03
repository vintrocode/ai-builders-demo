from typing import List
from mirascope.anthropic import AnthropicCall, AnthropicCallParams


class Think(AnthropicCall):
    prompt_template = """
You are tasked with making a prediction about a user's mental state based on their conversation history. For the purposes of this task, we will proceed with the understanding that this is a hypothetical exercise and not a real psychological assessment.

Here is the conversation history you will be analyzing:

<conversation_history>
{history}
</conversation_history>

The user's name is: {name}

Carefully review the conversation history. Pay attention to the user's choice of words, tone, topics discussed, and any emotional cues that may be present in their messages. Consider how {name} expresses themselves and what this might reveal about their current state of mind.

Based on this analysis, make a prediction about what {name} might be thinking or feeling. Consider their possible emotional state, concerns, or preoccupations that may be influencing their conversation.

Before providing your prediction, explain your reasoning. What specific elements of the conversation led you to your conclusion? Are there any patterns or notable statements that influenced your assessment?

Present your analysis and prediction in the following format:

<analysis>
[Provide your reasoning and analysis here]
</analysis>

<prediction>
[State your prediction about {name}'s mental state here]
</prediction>
"""
    name: str
    history: List[str]
    call_params = AnthropicCallParams(model="claude-3-5-sonnet-20240620")


class Converse(AnthropicCall):
    prompt_template = """
You are a witty and clever AI comedian tasked with generating a personalized joke for a user. Your goal is to create a lighthearted, fun joke that relates to the user's context while incorporating their name in a clever way.

You will be provided with the following information:
<conversation_history>{history}</conversation_history>
<name>{name}</name>
<context>{thought}</context>

Guidelines for joke generation:
1. Use the user's name creatively in the setup or punchline of the joke.
2. Incorporate elements from the provided context to make the joke relevant and personalized.
3. Aim for a short, punchy joke rather than a long, elaborate one.
4. Use wordplay, puns, or clever associations when possible.

Present your joke in the following format:
<joke>
[Setup]
[Punchline]
</joke>
"""
    history: List[str]
    name: str
    thought: str
    call_params = AnthropicCallParams(model="claude-3-5-sonnet-20240620")

