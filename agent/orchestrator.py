# agent/orchestrator.py
import json
import os
import re

from google import genai
from google.genai import types

from agent.prompts import build_research_prompt
from agent.schema import PersonProfile
from config import GEMINI_MODEL
from utils.logger import get_logger

logger = get_logger(__name__)


class PersonIntelAgent:
    """
    Orchestrates the full research pipeline.

    Uses Gemini with native Google Search grounding — no external search
    client needed. Gemini autonomously decides what to search, how many
    queries to run, and synthesises the results into a structured JSON profile.
    """

    def __init__(self) -> None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("GOOGLE_API_KEY must be set in your .env file.")
        self.client = genai.Client(api_key=api_key)
        self._search_tool = types.Tool(google_search=types.GoogleSearch())

    def run(
        self,
        name: str,
        selected_keys: list[str] | None = None,
        progress_callback=None,
    ) -> tuple[PersonProfile | None, str]:
        """
        Research a person and return a validated PersonProfile.

        Args:
            name:          Full name of the person to research.
            selected_keys: Dimension keys to include (None = all).
            progress_callback: Optional callable(step: str, pct: float).

        Returns:
            Tuple of (PersonProfile | None, raw_json_string).
        """
        if progress_callback:
            progress_callback("🔍 SOROT sedang menelusuri sumber publik...", 0.2)

        prompt = build_research_prompt(name, selected_keys)
        logger.info(f"Starting research for: {name!r} | dims: {selected_keys}")

        if progress_callback:
            progress_callback("🤖 Menganalisis dan menyusun profil...", 0.6)

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[self._search_tool],
                temperature=0.1,
            ),
        )

        if progress_callback:
            progress_callback("📋 Memvalidasi struktur data...", 0.9)

        raw_text = response.text.strip()

        # Strip markdown fences defensively
        raw_json = re.sub(
            r"^```(?:json)?\s*|\s*```$", "", raw_text, flags=re.MULTILINE
        ).strip()

        logger.info(f"Response received ({len(raw_json)} chars) for: {name!r}")

        try:
            profile = PersonProfile.model_validate(json.loads(raw_json))
            logger.info(f"Profile validated successfully for: {name!r}")
            return profile, raw_json
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(
                f"Parse failed for {name!r}: {exc}\n"
                f"Raw (first 500): {raw_json[:500]}"
            )
            return None, raw_json
