# SkillBridge Architecture

## Flow
CV Text → DocumentParser → ParsedDocument
JD Text → DocumentParser → ParsedDocument
                    ↓
            SemanticMatcher
            (sentence-transformers)
                    ↓
             MatchResult
                    ↓
          HiddenGemScorer
                    ↓
            GemScore + Report

## Key Design Decisions

### Why Semantic Matching?
Keyword ATS misses great candidates. "Orchestrated microservices"
should match "DevOps" — semantic embeddings make this possible.

### Hidden Gem Score Formula
total = (semantic * 0.4) + (coverage * 0.4)
      + experience_bonus + education_bonus
      + nonlinear_bonus - unmatched_penalty

### Non-linear Career Bonus
Candidates with skills BEYOND the JD requirements get rewarded.
This surfaces career-switchers and self-learners.

## Models Used
- Parsing: spaCy en_core_web_lg
- Matching: all-MiniLM-L6-v2 (fast, accurate for skill matching)