# CoursePath - A Semantic Academic Planning Engine

CoursePath is a data-driven academic planning system designed to generate optimized semester-level and multi-year course plans based on institutional requirements, major pathways, and student interests.

The project combines constraint satisfaction, preference modeling, and semantic topic matching to recommend balanced and goal-aligned course combinations. While inspired by AI recommendation systems, CoursePath emphasizes transparency, interpretability, and extensibility.

# Motivation

University course planning is a complex decision problem involving:
- prerequisite constraints
- time conflicts and unit limits
- major and breadth requirements
- workload balance
- long-term academic and career goals

Most existing tools treat these factors independently. CoursePath aims to unify them into a single optimization framework that can reason about short-term feasibility and long-term academic pathways.

# Core Idea

At its core, CoursePath models academic planning as a constraint-based optimization problem:

1. Generate feasible course combinations per semester
2. Filter combinations using hard constraints
3. Score combinations using weighted academic objectives
4. Select high-scoring plans sequentially across semesters

Semantic topic tags (e.g. genomics, statistics, programming) allow the system to align course recommendations with evolving academic interests and career goals such as bioinformatics, finance, or research.

# Project Architecture
coursepath/planner.py # Core planning logic
coursepath/data/courses.json # Normalized course dataset
coursepath/examples/sample_output.txt
coursepath/README.md

# Current Features

- Semester-level course combination generation
- Prerequisite checking
- Unit and time conflict validation
- Interest-aware scoring
- Ranked schedule recommendations

# Planned Extensions

- Berkeley course catalog ingestion
- BerkeleyTime workload and grade distribution integration
- RateMyProfessor teaching quality signals
- Multi-year planning with prerequisite forecasting
- Breadth requirement tracking
- CLI and web-based interfaces
- Explainable recommendations with score breakdowns

## Scoring Model (Simplified)

Each course combination is scored using a weighted linear model:
Score = w1 · interest_alignment + w2 · major_progress + w3 · workload_balance + w4 · teaching_quality + w5 · schedule_quality + w6 · breadth_coverage

Weights are adjustable and designed to be interpretable rather than opaque.

# Disclaimer

This project is a research and learning tool. It does not guarantee enrollment availability or institutional compliance and should not replace official academic advising.

# Author

Shirley  
UC Berkeley  
Interests: Molecular & Cell Biology, Data Science, Bioinformatics, Science Education
