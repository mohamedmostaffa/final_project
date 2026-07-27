"""
محوّلات صيغة تعريف الأدوات (Tool Schema Adapters).

كل provider محتاج شكل مختلف لتعريف الأداة، فبنحوّل من الصيغة الموحّدة
(TOOL_SPEC) اللي في tools/*.py لصيغة كل واحد منهم.
"""


def to_anthropic(spec: dict) -> dict:
    return {
        "name": spec["name"],
        "description": spec["description"],
        "input_schema": spec["parameters"],
    }


def to_openai_style(spec: dict) -> dict:
    """صالحة لـ Groq وأي API متوافق مع OpenAI (chat.completions + tools)."""
    return {
        "type": "function",
        "function": {
            "name": spec["name"],
            "description": spec["description"],
            "parameters": spec["parameters"],
        },
    }


def to_gemini(spec: dict) -> dict:
    return {
        "name": spec["name"],
        "description": spec["description"],
        "parameters": spec["parameters"],
    }
