import numpy as np
from dataclasses import dataclass, field
from typing import Optional
from src.parser.document_parser import ParsedDocument
from src.parser.skill_taxonomy import SKILL_TAXONOMY, get_skill

@dataclass
class SkillMatch:
    jd_requirement: str
    cv_evidence: str
    similarity_score: float
    match_type: str
    confidence: str

@dataclass
class MatchResult:
    skill_matches: list = field(default_factory=list)
    unmatched_requirements: list = field(default_factory=list)
    bonus_skills: list = field(default_factory=list)
    overall_semantic_score: float = 0.0
    coverage_score: float = 0.0

class SemanticMatcher:
    THRESHOLDS = {"high": 0.80, "medium": 0.60, "low": 0.40}

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            print("[SemanticMatcher] Model loaded.")
        except ImportError:
            print("[SemanticMatcher] Falling back to taxonomy matching.")

    def match(self, cv_doc: ParsedDocument, jd_doc: ParsedDocument) -> MatchResult:
        cv_phrases = self._extract_phrases(cv_doc)
        jd_phrases = self._extract_phrases(jd_doc)
        if not jd_phrases:
            return MatchResult()
        if self.model:
            return self._semantic_match(cv_phrases, jd_phrases)
        return self._taxonomy_match(cv_phrases, jd_phrases)

    def _extract_phrases(self, doc: ParsedDocument) -> list:
        phrases = set(doc.raw_skills_mentions)
        for skill in SKILL_TAXONOMY.values():
            for section_text in doc.sections.values():
                t = section_text.lower()
                if skill.name.lower() in t:
                    phrases.add(skill.name)
                for alias in skill.aliases:
                    if alias.lower() in t:
                        phrases.add(skill.name)
        return list(phrases)

    def _semantic_match(self, cv_phrases, jd_phrases) -> MatchResult:
        result = MatchResult()
        cv_emb = self.model.encode(cv_phrases, normalize_embeddings=True)
        jd_emb = self.model.encode(jd_phrases, normalize_embeddings=True)
        sim = np.dot(jd_emb, cv_emb.T)
        for i, jd_phrase in enumerate(jd_phrases):
            best_idx = int(np.argmax(sim[i]))
            score = float(sim[i][best_idx])
            if score >= self.THRESHOLDS["low"]:
                conf = "high" if score >= self.THRESHOLDS["high"] else "medium" if score >= self.THRESHOLDS["medium"] else "low"
                mtype = "exact" if jd_phrase.lower() == cv_phrases[best_idx].lower() else "semantic"
                result.skill_matches.append(SkillMatch(jd_phrase, cv_phrases[best_idx], round(score,3), mtype, conf))
            else:
                result.unmatched_requirements.append(jd_phrase)
        matched = len(result.skill_matches)
        total = len(jd_phrases)
        result.coverage_score = round(matched/total, 3) if total else 0.0
        result.overall_semantic_score = round(float(np.mean([m.similarity_score for m in result.skill_matches])), 3) if result.skill_matches else 0.0
        return result

    def _taxonomy_match(self, cv_phrases, jd_phrases) -> MatchResult:
        result = MatchResult()
        cv_skills = {get_skill(p) for p in cv_phrases if get_skill(p)}
        for phrase in jd_phrases:
            s = get_skill(phrase)
            if s and s in cv_skills:
                result.skill_matches.append(SkillMatch(phrase, s.name, 0.90, "taxonomy", "high"))
            else:
                result.unmatched_requirements.append(phrase)
        total = len(jd_phrases)
        result.coverage_score = round(len(result.skill_matches)/total, 3) if total else 0.0
        return result