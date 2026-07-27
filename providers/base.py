"""
BaseAgent: كلاس أساسي كل الـ providers بترث منه.

الجزء المشترك بينهم كله هنا (تنضيف نص JSON النهائي والتحقق منه بالـ schema).
كل provider بيعمل override لدالة check() بس، وبينفذ فيها الـ loop الخاص
بالـ API بتاعه.
"""

import json
from abc import ABC, abstractmethod

from schemas import FactCheckReport


class BaseAgent(ABC):
    @abstractmethod
    def check(self, claim_text: str, verbose: bool = True) -> FactCheckReport:
        """يشغّل الوكيل ويرجع تقرير تحقق منظّم."""
        raise NotImplementedError

    @staticmethod
    def parse_final_report(final_text: str) -> FactCheckReport:
        """
        ينضّف نص الرد النهائي (لو فيه ```json حواليه بالغلط) ويتحقق منه
        بالـ Pydantic schema. مشترك بين كل الـ providers.
        """
        cleaned = (final_text or "").strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
        cleaned = cleaned.strip()

        if not cleaned:
            raise ValueError("الموديل رجّع رد نهائي فاضي - مفيش JSON نقدر نتحقق منه.")

        data = json.loads(cleaned)
        return FactCheckReport(**data)
