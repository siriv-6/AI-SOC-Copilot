from pydantic import BaseModel
from typing import List


class ThreatAnalysis(BaseModel):
    attack_type: str
    severity: str
    confidence: float
    evidence: List[str]
    summary: str