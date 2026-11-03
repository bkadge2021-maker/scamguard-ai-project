from typing import List, Literal
from pydantic import BaseModel, Field

class ScamAnalysis(BaseModel):
    classification: Literal["Likely safe", "Suspicious", "Likely scam"]
    risk_score: int = Field(ge=0, le=100)
    scam_type: str
    intent: str
    evidence: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
