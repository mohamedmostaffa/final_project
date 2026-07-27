"""
GroqAgent: تنفيذ الوكيل باستخدام Groq API (موديلات مفتوحة زي Llama، سريعة ومجانية).

✅ ده كمان خيار مجاني - مفتاح API من console.groq.com من غير بطاقة بنكية.

يعتمد على مكتبة groq (متوافقة مع صيغة OpenAI tool-calling):
    pip install groq
"""

import json
import os

from groq import Groq

from providers.base import BaseAgent
from providers.registry import SYSTEM_PROMPT, TOOL_SPECS, MAX_TOOL_ITERATIONS, run_tool
from providers.schema_adapters import to_openai_style
from schemas import FactCheckReport

GROQ_TOOLS = [to_openai_style(spec) for spec in TOOL_SPECS]


class GroqAgent(BaseAgent):
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
        self.model = model or os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    def check(self, claim_text: str, verbose: bool = True) -> FactCheckReport:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": claim_text},
        ]

        for _ in range(MAX_TOOL_ITERATIONS):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=GROQ_TOOLS,
                tool_choice="auto",
            )
            message = response.choices[0].message

            if not message.tool_calls:
                return self.parse_final_report((message.content or "").strip())

            messages.append(message)

            for tool_call in message.tool_calls:
                tool_input = json.loads(tool_call.function.arguments or "{}")
                if verbose:
                    print(f"  [أداة] {tool_call.function.name}({tool_input})")
                result = run_tool(tool_call.function.name, tool_input)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        raise RuntimeError(
            f"الوكيل تجاوز الحد الأقصى للتكرارات ({MAX_TOOL_ITERATIONS}) من غير ما يوصل لتقرير نهائي."
        )
