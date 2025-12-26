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

# Scoring Model

Each course combination is scored using a weighted linear model:

Score = w1 · interest_alignment + w2 · teaching_quality + w3 · course difficulty

Weights are adjustable and designed to be interpretable rather than opaque.

# Building Weighted Topic Representation

Instead of modeling course topics as binary labels, this project represents each course using a weighted topic distribution. Each topic weight reflects the relative instructional emphasis of the course and the weights for a course approximately sum to 1.

This design captures the fact that many courses are interdisciplinary in nature and that different topics may contribute unequally to the learning experience. For example, an applied data science course may place greater weight on programming than on mathematical foundations. Using weighted topic vectors enables smoother and more realistic relevance scoring. Mathematically, course relevance is computed as a weighted dot product between the student’s normalized interest vector and the course’s topic vector, a standard approach in recommender systems and decision modeling.

Generally speaking, the evaluation system follows the following rule:
theory-heavy: receive higher value in math/statistics/algorithm
wet lab: receive higher value in lab & domain science
computation: receive higher value in python/r/bioinformatics
engineering: result in higher value in engineering/physics/math

Below is a list of scoring standards for each topic tag:

Python

Python weight reflects active computational use in assignments, labs, or projects.
A course receives Python spillover only if students write, debug, or analyze code, not merely if Python is recommended or optional.
0.5–0.7: Python is the primary medium of instruction (e.g., DATA C8, CS 61A)
0.2–0.4: Python is used to implement algorithms, analyze data, or run simulations
0.1 or none: Python appears only incidentally or in optional examples
Mathematics or statistics courses receive Python spillover only when computation is central, such as numerical linear algebra or simulation-based inference.

R

R weight represents statistical programming and data analysis, distinct from general programming.
R is not treated as interchangeable with Python.
0.5–0.7: R is the main analytical tool (upper-division statistics, data labs)
0.2–0.4: R supports statistical modeling alongside theory
0.0: No spillover unless R is explicitly used
This separation allows accurate modeling of data-science-focused tracks versus general CS tracks.

Algorithm

Algorithm weight captures formal reasoning about procedures, efficiency, and correctness, not just coding.
0.6–0.8: Courses centered on algorithm design, proofs, or complexity (CS 61B, CS 70)
0.3–0.5: Algorithms are implemented or analyzed but not the sole focus
0.1–0.2: Procedural reasoning appears as a secondary skill
Algorithm spillover is assigned to math courses only when discrete or combinatorial reasoning is emphasized.

Bioinformatics

Bioinformatics weight reflects computational analysis of biological data, not biological theory alone.
0.4–0.6: Genomic, transcriptomic, or systems-level data analysis
0.2–0.3: Biology courses with explicit data-driven components
0.0: No spillover unless computation on biological data is required
This prevents traditional wet-lab biology from being mislabeled as bioinformatics.

Biochemistry

Biochemistry weight measures molecular-level chemical reasoning applied to biological systems.
0.5–0.7: Reaction mechanisms, molecular interactions, structure–function
0.2–0.4: Supporting chemical understanding for biological processes
0.0: No spillover without molecular focus
This tag is distinct from genetics and lab work, even when courses overlap in content.

Genetics

Genetics weight reflects inheritance, gene regulation, and molecular genetics reasoning.
0.5–0.7: Core genetics and gene expression
0.2–0.4: Genetics used as a conceptual framework within biology
0.0: No spillover unless genetics is explicitly taught
Genetics spillover may coexist with bioinformatics, but the two represent conceptual vs. computational emphasis.

Physics

Physics weight captures model-based reasoning about physical systems.
0.7–0.8: Mechanics, E&M, or waves as the primary focus
0.2–0.3: Supporting physical intuition for engineering or biology
0.0: No spillover without formal physics modeling
Physics spillover does not imply engineering unless design constraints are introduced.

Math

Math weight represents formal mathematical reasoning, including proofs, abstraction, and symbolic manipulation.
0.7–1.0: Proof-based or theory-heavy math courses
0.3–0.5: Applied mathematics used to support other disciplines
0.1–0.2: Mathematical tools without deep abstraction
Math spillover does not automatically generate programming weight unless computation is central.

Lab

Lab weight reflects hands-on experimental design, data collection, and protocol execution.
0.4–0.6: Dedicated laboratory courses
0.2–0.3: Significant experimental components
0.0: No spillover for theory-only courses
Lab is treated independently to capture workload and experiential learning.

Statistics

Statistics weight measures probabilistic reasoning, inference, and uncertainty modeling.
0.6–0.8: Statistical modeling and inference as the core objective
0.3–0.5: Statistics used to support another discipline
0.0: No spillover without formal statistical thinking
Statistics spillover may coexist with Python or R but remains conceptually distinct.

Engineering

Engineering weight reflects design-oriented problem solving under constraints.
0.5–0.7: Systems design, optimization, or applied modeling
0.2–0.4: Engineering reasoning supporting theory
0.0: No spillover without design or applied constraints
Engineering is intentionally separated from physics and math to preserve semantic clarity.

For the tag design, topic overlap is expected and intentional. Each tag represents a different dimension of skill, not a mutually exclusive category. Because weights are normalized, scoring is linear, and combinations are evaluated holistically, overlap does not inflate scores unfairly. Instead, it reflects multidisciplinary richness, which is precisely what a four-year academic planner should reward.

#Interactively Building Interest Profiles
The program lets users build a personalized interest profile interactively, which guides course recommendations. It first collects all available topics from the course dataset, then prompts the user to rate their interest in each topic on a scale (e.g., 0.0–1.0). These ratings are stored in a dictionary and used to score semester plans, prioritizing courses that match the user’s preferences. This approach ensures flexibility, personalization, and automatic support for new topics without manual updates.

# Disclaimer

This project is a research and learning tool. It does not guarantee enrollment availability or institutional compliance and should not replace official academic advising.

# Author

Shirley Wu
UC Berkeley  
Interests: Molecular & Cell Biology, Data Science, Bioinformatics, Science Education
