from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Skill:
    name: str
    category: str
    aliases: list = field(default_factory=list)

SKILL_TAXONOMY = {
    "python": Skill("Python", "technical", ["py", "python3"]),
    "javascript": Skill("JavaScript", "technical", ["js", "nodejs", "node.js"]),
    "sql": Skill("SQL", "technical", ["mysql", "postgresql", "postgres"]),
    "machine_learning": Skill("Machine Learning", "technical", ["ml", "predictive modeling", "statistical modeling"]),
    "deep_learning": Skill("Deep Learning", "technical", ["neural networks", "cnn", "rnn", "lstm"]),
    "nlp": Skill("NLP", "technical", ["natural language processing", "text mining", "sentiment analysis"]),
    "devops": Skill("DevOps", "technical", ["ci/cd", "docker", "kubernetes", "containerization"]),
    "cloud": Skill("Cloud", "technical", ["aws", "azure", "gcp", "google cloud", "serverless"]),
    "data_engineering": Skill("Data Engineering", "technical", ["etl", "airflow", "spark", "kafka", "dbt"]),
    "leadership": Skill("Leadership", "soft", ["led", "managed", "directed", "team lead", "people manager"]),
    "mentoring": Skill("Mentoring", "soft", ["mentored", "coached", "trained", "onboarded"]),
    "communication": Skill("Communication", "soft", ["presentation", "public speaking", "storytelling"]),
    "agile": Skill("Agile", "process", ["scrum", "kanban", "sprint", "lean"]),
    "product_management": Skill("Product Management", "soft", ["product roadmap", "product owner", "gtm"]),
}

def get_skill(mention: str) -> Optional[Skill]:
    n = mention.lower().strip()
    if n in SKILL_TAXONOMY:
        return SKILL_TAXONOMY[n]
    for skill in SKILL_TAXONOMY.values():
        if n in [a.lower() for a in skill.aliases]:
            return skill
    return None