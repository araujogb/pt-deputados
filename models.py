from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class Commission(BaseModel):
    """One parliamentary commission with optional role"""
    name: str
    role: Optional[str] = None   # e.g. "Presidente", "Vice-Presidente", "Suplente"

class Deputy(BaseModel):
    """Full structured data for one deputy"""
    bid: int
    short_name: str
    full_name: str = ""
    birth_date: Optional[date] = None
    circle: str
    party: str
    education: List[str] = Field(default_factory=list)
    profession: Optional[str] = None
    previous_cargos: List[str] = Field(default_factory=list)
    current_commissions: List[Commission] = Field(default_factory=list)
    bio_url: str
    photo_url: Optional[str] = None
    last_updated: str = Field(default_factory=lambda: date.today().isoformat())
