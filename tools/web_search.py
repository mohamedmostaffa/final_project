"""
أداة البحث على الويب (Web Search Tool).

في الوضع الحقيقي: تستخدم Tavily API (https://tavily.com) - بسيط ورخيص ومناسب
لوكلاء AI. لو حابب تستبدلها بـ SerpAPI أو Google Custom Search، غيّر فقط
دالة `_real_search` وسيب باقي الكود زي ما هو.

في وضع mock (لو مفيش TAVILY_API_KEY): بترجع نتائج تجريبية ثابتة عشان تقدر
تختبر تدفق الوكيل (agent flow) كامل من غير ما تدفع فلوس أو تحتاج مفتاح فعلي.
"""

import os
import requests
from urllib.parse import urlparse


TAVILY_ENDPOINT = "https://api.tavily.com/search"


def _extract_domain(url: str) -> str:
    """يستخرج الدومين من رابط، مع إزالة www. لو موجودة."""
    netloc = urlparse(url).netloc
    return netloc[4:] if netloc.startswith("www.") else netloc


def _real_search(query: str, max_results: int = 5) -> list[dict]:
    api_key = os.environ.get("TAVILY_API_KEY")
    response = requests.post(
        TAVILY_ENDPOINT,
        json={
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": False,
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("results", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "domain": _extract_domain(item.get("url", "")),
                "snippet": item.get("content", "")[:500],
                "published_date": item.get("published_date"),
            }
        )
    return results


def _mock_search(query: str, max_results: int = 5) -> list[dict]:
    """نتائج تجريبية ثابتة لاختبار تدفق الوكيل بدون مفتاح API حقيقي."""
    return [
        {
            "title": f"[MOCK] نتيجة بحث تجريبية متعلقة بـ: {query}",
            "url": "https://example.com/mock-article-1",
            "domain": "example.com",
            "snippet": (
                "هذه نتيجة تجريبية (mock) لأنه لا يوجد TAVILY_API_KEY في متغيرات "
                "البيئة. ضع مفتاح Tavily حقيقي في ملف .env للحصول على نتائج بحث فعلية."
            ),
            "published_date": None,
        },
        {
            "title": f"[MOCK] مصدر ثانٍ تجريبي عن: {query}",
            "url": "https://example.org/mock-article-2",
            "domain": "example.org",
            "snippet": "نتيجة تجريبية ثانية لأغراض اختبار منطق مقارنة المصادر فقط.",
            "published_date": None,
        },
    ][:max_results]


def web_search(query: str, max_results: int = 5) -> dict:
    """
    ينفّذ بحثًا على الويب ويرجع نتائج منظّمة.

    Returns:
        dict فيه "mode" (real/mock) و "results" (list[dict])
    """
    if os.environ.get("TAVILY_API_KEY"):
        try:
            results = _real_search(query, max_results)
            return {"mode": "real", "query": query, "results": results}
        except requests.RequestException as exc:
            return {
                "mode": "error",
                "query": query,
                "results": [],
                "error": str(exc),
            }
    return {"mode": "mock", "query": query, "results": _mock_search(query, max_results)}


# تعريف الأداة بصيغة موحّدة (canonical) - كل مزوّد (Anthropic/Gemini/Groq) بيحوّلها
# لصيغته الخاصة عن طريق providers/schema_adapters.py
TOOL_SPEC = {
    "name": "web_search",
    "description": (
        "ابحث على الويب عن أخبار أو معلومات متعلقة بادعاء معيّن، عشان تتحقق "
        "هل فيه مصادر إخبارية موثوقة بتأكد أو بتنفي الخبر ده. استخدمها أكتر "
        "من مرة بصياغات مختلفة لو النتيجة الأولى مش كافية."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "نص البحث (يفضل بالعربية والإنجليزية لو الخبر عالمي)",
            },
            "max_results": {
                "type": "integer",
                "description": "عدد النتائج المطلوبة (افتراضي 5)",
            },
        },
        "required": ["query"],
    },
}
