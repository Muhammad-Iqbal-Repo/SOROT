# agent/schema.py
from pydantic import BaseModel, Field
from typing import Optional


class FamilyMember(BaseModel):
    name: str
    relation: str                          # e.g., "Istri", "Anak", "Ayah"
    role: Optional[str] = None             # e.g., "Anggota DPR RI", "Komisaris"
    notes: Optional[str] = None


class CorporateAffiliation(BaseModel):
    entity_name: str
    role: Optional[str] = None             # e.g., "Komisaris Utama", "Pemegang Saham"
    group: Optional[str] = None            # e.g., "Grup Bakrie", "Grup Salim"


class TniPolriInfo(BaseModel):
    is_tni_polri: bool = False
    branch: Optional[str] = None           # e.g., "TNI AD", "POLRI"
    last_rank: Optional[str] = None        # e.g., "Jenderal", "Komisaris Jenderal"
    status: Optional[str] = None           # "Aktif" or "Purnawirawan"


class PersonProfile(BaseModel):
    full_name: str
    also_known_as: list[str] = Field(default_factory=list)

    # Vital status
    is_alive: Optional[bool] = None
    death_info: Optional[str] = None       # Context if deceased

    # Roles & Positions
    current_roles: list[str] = Field(default_factory=list)
    past_roles: list[str] = Field(default_factory=list)

    # Special Government Classifications
    is_minister: bool = False
    is_deputy_minister: bool = False
    is_dpr_member: bool = False
    is_dprd_member: bool = False
    is_staf_khusus: bool = False
    is_high_official: bool = False

    # TNI/Polri
    tni_polri: TniPolriInfo = Field(default_factory=TniPolriInfo)

    # Political
    party_affiliations: list[str] = Field(default_factory=list)
    political_notes: Optional[str] = None

    # Family
    family_members: list[FamilyMember] = Field(default_factory=list)

    # Corporate
    corporate_affiliations: list[CorporateAffiliation] = Field(default_factory=list)

    # Confidence & metadata
    sources: list[str] = Field(default_factory=list)
    confidence_level: str = "medium"       # "high" | "medium" | "low"
    analyst_notes: Optional[str] = None
