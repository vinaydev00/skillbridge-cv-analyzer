from dataclasses import dataclass
from src.parser.document_parser import ParsedDocument
from src.matcher.semantic_matcher import MatchResult

@dataclass
class GemScore:
    total_score: float
    semantic_score: float
    coverage_score: float
    experience_bonus: float
    education_bonus: float
    nonlinear_bonus: float
    verdict: str
    explanation: list

class HiddenGemScorer:
    """
    Scores candidates beyond keyword matching.
    Rewards non-linear careers, transferable skills, self-learning.
    """

    VERDICT_THRESHOLDS = {
        "💎 Hidden Gem": 0.80,
        "⭐ Strong Match": 0.65,
        "✅ Good Fit": 0.50,
        "🔍 Partial Match": 0.35,
        "❌ Not a Fit": 0.0,
    }

    def score(self, cv_doc: ParsedDocument, match_result: MatchResult) -> GemScore:
        explanation = []

        # Base scores from matcher
        semantic = match_result.overall_semantic_score
        coverage = match_result.coverage_score

        # Experience bonus
        exp_bonus = 0.0
        if cv_doc.years_of_experience:
            if cv_doc.years_of_experience >= 10:
                exp_bonus = 0.10
                explanation.append(f"✓ {cv_doc.years_of_experience}+ years experience (+10%)")
            elif cv_doc.years_of_experience >= 5:
                exp_bonus = 0.05
                explanation.append(f"✓ {cv_doc.years_of_experience} years experience (+5%)")

        # Education bonus
        edu_bonus = 0.0
        edu_ranks = {"phd": 0.08, "master": 0.05, "msc": 0.05, "mba": 0.05, "bachelor": 0.02}
        if cv_doc.education_level in edu_ranks:
            edu_bonus = edu_ranks[cv_doc.education_level]
            explanation.append(f"✓ Education: {cv_doc.education_level} (+{int(edu_bonus*100)}%)")

        # Non-linear career bonus (bonus skills beyond JD requirements)
        nonlinear_bonus = 0.0
        if match_result.bonus_skills:
            nonlinear_bonus = min(len(match_result.bonus_skills) * 0.02, 0.10)
            explanation.append(f"✓ {len(match_result.bonus_skills)} bonus skills detected (+{int(nonlinear_bonus*100)}%)")

        # Unmatched penalty
        unmatched_ratio = len(match_result.unmatched_requirements) / max(
            len(match_result.skill_matches) + len(match_result.unmatched_requirements), 1)
        penalty = round(unmatched_ratio * 0.15, 3)
        if penalty > 0:
            explanation.append(f"✗ {len(match_result.unmatched_requirements)} unmatched requirements (-{int(penalty*100)}%)")

        # Total
        total = round(min((semantic * 0.4) + (coverage * 0.4) + exp_bonus + edu_bonus + nonlinear_bonus - penalty, 1.0), 3)

        # Verdict
        verdict = "❌ Not a Fit"
        for label, threshold in self.VERDICT_THRESHOLDS.items():
            if total >= threshold:
                verdict = label
                break

        # Match highlights
        for m in match_result.skill_matches[:3]:
            explanation.append(f"→ '{m.jd_requirement}' matched via '{m.cv_evidence}' ({m.match_type}, {m.confidence})")

        return GemScore(
            total_score=total,
            semantic_score=semantic,
            coverage_score=coverage,
            experience_bonus=exp_bonus,
            education_bonus=edu_bonus,
            nonlinear_bonus=nonlinear_bonus,
            verdict=verdict,
            explanation=explanation,
        )