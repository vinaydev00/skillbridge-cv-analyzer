import pytest
from src.scorer.hidden_gem_scorer import HiddenGemScorer, GemScore
from src.matcher.semantic_matcher import MatchResult, SkillMatch
from src.parser.document_parser import ParsedDocument

@pytest.fixture
def scorer():
    return HiddenGemScorer()

@pytest.fixture
def strong_cv():
    doc = ParsedDocument(raw_text="", doc_type="cv")
    doc.years_of_experience = 8.0
    doc.education_level = "master"
    return doc

@pytest.fixture
def strong_match():
    result = MatchResult()
    result.skill_matches = [
        SkillMatch("Python", "Python", 0.95, "exact", "high"),
        SkillMatch("Machine Learning", "ML", 0.88, "semantic", "high"),
        SkillMatch("Leadership", "Led teams", 0.75, "semantic", "medium"),
    ]
    result.bonus_skills = ["Docker", "AWS", "NLP"]
    result.overall_semantic_score = 0.86
    result.coverage_score = 0.90
    return result

def test_score_returns_gem_score(scorer, strong_cv, strong_match):
    result = scorer.score(strong_cv, strong_match)
    assert isinstance(result, GemScore)

def test_high_score_for_strong_candidate(scorer, strong_cv, strong_match):
    result = scorer.score(strong_cv, strong_match)
    assert result.total_score >= 0.60

def test_verdict_not_empty(scorer, strong_cv, strong_match):
    result = scorer.score(strong_cv, strong_match)
    assert result.verdict != ""

def test_explanation_populated(scorer, strong_cv, strong_match):
    result = scorer.score(strong_cv, strong_match)
    assert len(result.explanation) > 0

def test_bonus_skills_reflected(scorer, strong_cv, strong_match):
    result = scorer.score(strong_cv, strong_match)
    assert result.nonlinear_bonus > 0