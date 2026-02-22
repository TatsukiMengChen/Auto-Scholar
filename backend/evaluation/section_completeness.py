import re
import unicodedata

from backend.constants import (
    REQUIRED_SECTIONS_EN,
    REQUIRED_SECTIONS_ZH,
    SECTION_ALIASES,
)
from backend.evaluation.schemas import SectionCompletenessResult
from backend.schemas import DraftOutput


def _normalize_heading(heading: str) -> str:
    normalized = unicodedata.normalize("NFKC", heading)
    normalized = re.sub(r"^[\d\.\s]+", "", normalized)
    normalized = re.sub(r"[^\w\s]", "", normalized)
    return normalized.strip().lower()


def _matches_required(heading: str, required: str) -> bool:
    norm_heading = _normalize_heading(heading)
    norm_required = _normalize_heading(required)

    if norm_required in norm_heading or norm_heading in norm_required:
        return True

    aliases = SECTION_ALIASES.get(required, [])
    for alias in aliases:
        norm_alias = _normalize_heading(alias)
        if norm_alias in norm_heading or norm_heading in norm_alias:
            return True

    return False


def evaluate_section_completeness(
    draft: DraftOutput, language: str = "en"
) -> SectionCompletenessResult:
    required = REQUIRED_SECTIONS_EN if language == "en" else REQUIRED_SECTIONS_ZH

    present_headings = [section.heading for section in draft.sections]
    matched_required: set[str] = set()
    matched_present: set[str] = set()

    for req in required:
        for heading in present_headings:
            if _matches_required(heading, req):
                matched_required.add(req)
                matched_present.add(heading)
                break

    missing = [r for r in required if r not in matched_required]
    extra = [h for h in present_headings if h not in matched_present]

    return SectionCompletenessResult(
        required_sections=list(required),
        present_sections=present_headings,
        missing_sections=missing,
        extra_sections=extra,
    )
