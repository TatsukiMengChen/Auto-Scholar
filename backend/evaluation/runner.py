from backend.evaluation.academic_style import calculate_academic_style
from backend.evaluation.citation_metrics import (
    calculate_citation_precision,
    calculate_citation_recall,
)
from backend.evaluation.cost_tracker import parse_cost_from_logs
from backend.evaluation.human_ratings import get_rating_summary
from backend.evaluation.schemas import EvaluationResult
from backend.evaluation.section_completeness import evaluate_section_completeness
from backend.schemas import ClaimVerificationSummary, DraftOutput, PaperMetadata


def run_evaluation(
    thread_id: str,
    draft: DraftOutput,
    approved_papers: list[PaperMetadata],
    logs: list[str],
    language: str = "en",
    claim_verification: ClaimVerificationSummary | None = None,
) -> EvaluationResult:
    num_approved = len(approved_papers)

    citation_precision = calculate_citation_precision(draft, num_approved)
    citation_recall = calculate_citation_recall(draft, approved_papers)
    section_completeness = evaluate_section_completeness(draft, language)
    academic_style = calculate_academic_style(draft, language)
    cost_efficiency = parse_cost_from_logs(logs)

    claim_support_rate = 0.0
    if claim_verification and claim_verification.total_verifications > 0:
        claim_support_rate = (
            claim_verification.entails_count / claim_verification.total_verifications
        )

    human_ratings = get_rating_summary(thread_id)

    return EvaluationResult(
        thread_id=thread_id,
        citation_precision=citation_precision,
        citation_recall=citation_recall,
        claim_support_rate=claim_support_rate,
        section_completeness=section_completeness,
        academic_style=academic_style,
        cost_efficiency=cost_efficiency,
        human_ratings=human_ratings,
        language=language,
        paper_count=num_approved,
    )
