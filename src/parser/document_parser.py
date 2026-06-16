import re
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ParsedDocument:
    raw_text: str
    doc_type: str
    sections: dict = field(default_factory=dict)
    raw_skills_mentions: list = field(default_factory=list)
    years_of_experience: Optional[float] = None
    education_level: Optional[str] = None

class DocumentParser:
    CV_SECTION_PATTERNS = [
        r"(experience|work history|employment)",
        r"(education|academic|qualifications)",
        r"(skills|technical skills|competencies)",
        r"(projects|portfolio|achievements)",
        r"(summary|objective|about me|profile)",
    ]
    EDUCATION_LEVELS = {
        "phd": 5, "master": 4, "msc": 4, "mba": 4,
        "bachelor": 3, "bsc": 3, "diploma": 1,
    }

    def parse(self, text: str, doc_type: str = "cv") -> ParsedDocument:
        doc = ParsedDocument(raw_text=text, doc_type=doc_type)
        doc.sections = self._extract_sections(text)
        doc.years_of_experience = self._extract_years(text)
        doc.education_level = self._extract_education(text)
        doc.raw_skills_mentions = self._extract_skills(text)
        return doc

    def _extract_sections(self, text: str) -> dict:
        sections = {}
        lines = text.split("\n")
        current, content = "header", []
        for line in lines:
            s = line.strip().lower()
            matched = None
            for p in self.CV_SECTION_PATTERNS:
                if re.search(p, s) and len(s) < 60:
                    matched = re.search(p, s).group(1)
                    break
            if matched:
                sections[current] = "\n".join(content).strip()
                current, content = matched, []
            else:
                content.append(line)
        sections[current] = "\n".join(content).strip()
        return sections

    def _extract_years(self, text: str) -> Optional[float]:
        m = re.findall(r"(\d+)\+?\s*years?\s+of\s+experience", text, re.IGNORECASE)
        return float(m[0]) if m else None

    def _extract_education(self, text: str) -> Optional[str]:
        t = text.lower()
        best, rank = None, -1
        for level, r in self.EDUCATION_LEVELS.items():
            if level in t and r > rank:
                best, rank = level, r
        return best

    def _extract_skills(self, text: str) -> list:
        raw = re.findall(r"\b([A-Z][a-zA-Z0-9+#./]*(?:\s+[A-Z][a-zA-Z0-9+#./]*){0,2})\b", text)
        stops = {"I","We","The","A","An","In","At","For","And","Or"}
        return list(set([m.strip() for m in raw if m not in stops and len(m) > 1]))