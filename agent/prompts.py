# agent/prompts.py
from config import RESEARCH_DIMENSIONS


def build_research_prompt(name: str, selected_keys: list[str] | None = None) -> str:
    """
    Builds a Gemini research prompt for the given person.

    Args:
        name:          Full name of the person to research.
        selected_keys: Optional list of dimension keys from RESEARCH_DIMENSIONS
                       to include. Defaults to all dimensions if None.

    Returns:
        A fully formatted prompt string ready to send to Gemini.
    """
    keys = selected_keys if selected_keys else list(RESEARCH_DIMENSIONS.keys())

    dimensions_text = "\n".join(
        f"  {i + 1}. {RESEARCH_DIMENSIONS[k][1]}"
        for i, k in enumerate(keys)
        if k in RESEARCH_DIMENSIONS
    )

    return f"""
Lakukan riset mendalam menggunakan pencarian web tentang tokoh publik Indonesia berikut:

**Nama:** {name}

Temukan informasi mengenai:
{dimensions_text}

Panduan penting:
- Gunakan hanya fakta yang didukung sumber publik yang dapat diverifikasi
- Jangan mengarang informasi yang tidak ditemukan di sumber manapun
- Jika suatu informasi tidak tersedia, biarkan field tersebut null atau array kosong
- Berikan confidence_level: "high" jika banyak sumber konsisten mengonfirmasi,
  "medium" jika hanya sebagian, "low" jika hanya satu sumber atau meragukan
- Sertakan URL sumber asli di field "sources"
- Gunakan analyst_notes untuk mencatat ambiguitas atau peringatan penting

Kembalikan HANYA objek JSON yang valid (tanpa markdown code block, tanpa teks tambahan)
yang sesuai dengan skema berikut persis:

{{
  "full_name": "string",
  "also_known_as": ["string"],
  "is_alive": true,
  "death_info": null,
  "current_roles": ["string"],
  "past_roles": ["string"],
  "is_minister": false,
  "is_deputy_minister": false,
  "is_dpr_member": false,
  "is_dprd_member": false,
  "is_staf_khusus": false,
  "is_high_official": false,
  "tni_polri": {{
    "is_tni_polri": false,
    "branch": null,
    "last_rank": null,
    "status": null
  }},
  "party_affiliations": ["string"],
  "political_notes": null,
  "family_members": [
    {{
      "name": "string",
      "relation": "string",
      "role": null,
      "notes": null
    }}
  ],
  "corporate_affiliations": [
    {{
      "entity_name": "string",
      "role": null,
      "group": null
    }}
  ],
  "sources": ["https://..."],
  "confidence_level": "medium",
  "analyst_notes": null
}}
"""
