import pytest
from src.parser.document_parser import DocumentParser, ParsedDocument

@pytest.fixture
def parser():
    return DocumentParser()

@pytest.fixture
def sample_cv():
    return """
John Doe - Software Developer

SUMMARY
Python developer with 5 years of experience in machine learning and data engineering.

SKILLS
Python, SQL, Machine Learning, Docker, AWS

EXPERIENCE
Senior Developer | TechCorp | 2020 - Present
- Led cross-functional teams of 5 engineers
- Built ETL pipelines using Airflow and Spark
- Mentored 3 junior developers

EDUCATION
Master of Science in Computer Science | IIT Delhi | 2019
"""

def test_parse_returns_parsed_document(parser, sample_cv):
    result = parser.parse(sample_cv, "cv")
    assert isinstance(result, ParsedDocument)
    assert result.doc_type == "cv"

def test_sections_extracted(parser, sample_cv):
    result = parser.parse(sample_cv, "cv")
    assert len(result.sections) > 0

def test_years_of_experience_extracted(parser):
    text = "I have 5 years of experience in Python."
    result = parser.parse(text, "cv")
    assert result.years_of_experience == 5.0

def test_education_level_extracted(parser, sample_cv):
    result = parser.parse(sample_cv, "cv")
    assert result.education_level == "master"

def test_skills_extracted(parser, sample_cv):
    result = parser.parse(sample_cv, "cv")
    assert len(result.raw_skills_mentions) > 0