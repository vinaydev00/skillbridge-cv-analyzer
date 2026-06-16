"""
SkillBridge CV Analyzer - Main CLI Entry Point
Usage: python -m src.main --cv path/to/cv.txt --jd path/to/jd.txt
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from src.parser.document_parser import DocumentParser
from src.matcher.semantic_matcher import SemanticMatcher
from src.scorer.hidden_gem_scorer import HiddenGemScorer

console = Console()

@click.command()
@click.option("--cv", required=True, help="Path to CV text file")
@click.option("--jd", required=True, help="Path to Job Description text file")
@click.option("--model", default="all-MiniLM-L6-v2", help="Sentence transformer model")
def analyze(cv: str, jd: str, model: str):
    """Analyze a CV against a Job Description using SkillBridge."""

    console.print(Panel.fit("🌉 [bold cyan]SkillBridge CV Analyzer[/bold cyan]", box=box.DOUBLE))

    # Parse
    console.print("\n[yellow]Parsing documents...[/yellow]")
    parser = DocumentParser()
    cv_doc = parser.parse(Path(cv).read_text(encoding="utf-8"), "cv")
    jd_doc = parser.parse(Path(jd).read_text(encoding="utf-8"), "jd")

    console.print(f"✓ CV sections found: {list(cv_doc.sections.keys())}")
    console.print(f"✓ JD sections found: {list(jd_doc.sections.keys())}")

    # Match
    console.print("\n[yellow]Running semantic matching...[/yellow]")
    matcher = SemanticMatcher(model_name=model)
    result = matcher.match(cv_doc, jd_doc)

    # Score
    scorer = HiddenGemScorer()
    gem = scorer.score(cv_doc, result)

    # Display Results
    console.print(Panel.fit(f"[bold green]{gem.verdict}[/bold green]\nTotal Score: [bold]{gem.total_score:.0%}[/bold]"))

    # Score breakdown table
    table = Table(title="Score Breakdown", box=box.ROUNDED)
    table.add_column("Component", style="cyan")
    table.add_column("Score", style="green")
    table.add_row("Semantic Match", f"{gem.semantic_score:.0%}")
    table.add_row("Skill Coverage", f"{gem.coverage_score:.0%}")
    table.add_row("Experience Bonus", f"+{gem.experience_bonus:.0%}")
    table.add_row("Education Bonus", f"+{gem.education_bonus:.0%}")
    table.add_row("Non-linear Bonus", f"+{gem.nonlinear_bonus:.0%}")
    console.print(table)

    # Explanation
    console.print("\n[bold]Analysis:[/bold]")
    for line in gem.explanation:
        console.print(f"  {line}")

    # Unmatched
    if result.unmatched_requirements:
        console.print(f"\n[red]Missing skills:[/red] {', '.join(result.unmatched_requirements[:5])}")

    # Bonus skills
    if result.bonus_skills:
        console.print(f"\n[cyan]Bonus skills:[/cyan] {', '.join(result.bonus_skills[:5])}")

if __name__ == "__main__":
    analyze()