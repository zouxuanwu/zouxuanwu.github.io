import json
with open("courses.json") as f:
    courses = json.load(f)
import itertools
from itertools import combinations
import heapq

def check_requirements(requirements, taken_courses):
    if isinstance(requirements, str):
        return requirements in taken_courses
    elif "and" in requirements:
        return all(check_requirements(r, taken_courses) for r in requirements["and"])
    elif "or" in requirements:
        return any(check_requirements(r, taken_courses) for r in requirements["or"])
    else:
        raise ValueError("Unknown requirement format")

def prereqs_met(course_name, taken_courses):
    course = courses[course_name]
    if course["prerequisites"] is None:
        return True
    return check_requirements(course["prerequisites"], taken_courses)
  
def valid_schedule(schedule, min_units=8, max_units=12):
    total_units = 0
    times = set()
    for course_name in schedule:
        course = courses[course_name]
        total_units += course["units"]
    return min_units <= total_units <= max_units
  
def offered_in_term(course, term):
    return term in course["terms_offered"]

def interest_alignment(schedule, interest_profile):
    score = 0
    for course_name in schedule:
        topics = courses[course_name]["topics"]
        for t, weight in topics.items():
            score += weight * interest_profile.get(t, 0)
    return score / len(schedule) if schedule else 0

def collect_topics(courses):
    all_topics = set()
    for c in courses.values():
        all_topics.update(c.get("topics", {}).keys())
    return list(all_topics)
    
def get_interest_profile(topics):
    print("Rate your interest in the following topics from 0 to 1 (e.g., 0.8):")
    profile = {}
    for t in topics:
        while True:
            try:
                val = float(input(f"{t}: "))
                if 0 <= val <= 1:
                    profile[t] = val
                    break
                else:
                    print("Please enter a number between 0 and 1.")
            except ValueError:
                print("Invalid input. Enter a number.")
    return profile
    
def score_schedule(schedule, interest_profile, weights):
    interest = interest_alignment(schedule, interest_profile)

    avg_difficulty = sum(courses[c]["difficulty"] for c in schedule) / len(schedule)
    avg_prof_rating = sum(courses[c]["professor_rating"] for c in schedule) / len(schedule)

    return (
        weights["interest"] * interest
        - weights["difficulty"] * avg_difficulty
        + weights["professor"] * avg_prof_rating
    )
    
def get_weights():
    return {
        "interest": float(input("Weight for interest (e.g. 1.0): ")),
        "difficulty": float(input("Weight for difficulty (e.g. 0.5): ")),
        "professor": float(input("Weight for professor rating (e.g. 0.3): "))
    }

def generate_semester_plans(
    completed_courses,
    interest_profile,
    term=None,
    min_units=8,
    max_units=12,
    weights=None,
    top_k=5
):
    if weights is None:
        weights = get_weights()

    available = [
        c for c in courses
        if c not in completed_courses
        and prereqs_met(c, completed_courses)
        and (term is None or offered_in_term(courses[c], term))
    ]

    heap = []

    for r in range(1, len(available) + 1):
        for schedule in itertools.combinations(available, r):
            if not valid_schedule(schedule, min_units, max_units):
                continue

            score = score_schedule(schedule, interest_profile, weights)

            heapq.heappush(heap, (score, schedule))
            if len(heap) > top_k:
                heapq.heappop(heap)

    return [
        {"courses": s, "score": sc}
        for sc, s in sorted(heap, reverse=True)
    ]

# Example run

if __name__ == "__main__":
    completed_courses = []

    topics = collect_topics(courses)
    interest_profile = get_interest_profile(topics)

    top_plans = generate_semester_plans(
        completed_courses,
        interest_profile,
        course_count=3,
    )

    for i, (score, plan) in enumerate(top_plans, 1):
        print(f"\nPlan {i} | Score: {round(score, 3)}")
        for c in plan:
            print("  -", c)

# test blocks

def test_check_requirements():
    taken = ["MATH 51", "PHYSICS 7A", "BIOENG 11"]
    req1 = "MATH 51"
    req2 = {"and": ["MATH 51", "PHYSICS 7A"]}
    req3 = {"or": ["BIOLOGY 1A", "BIOENG 11"]}

    assert check_requirements(req1, taken) == True
    assert check_requirements(req2, taken) == True
    assert check_requirements(req3, taken) == True
    print("check_requirements tests passed!")

def test_valid_schedule():
    schedule = ["BIOENG 103", "DATA C8"]
    print("Total units:", sum(courses[c]["units"] for c in schedule))
    print("Valid schedule?", valid_schedule(schedule))

def test_generate_semester_plans():
    completed_courses = ["MATH 51", "PHYSICS 7A"]
    interest_profile = {"genomics": 1, "statistics": 0.8}
    plans = generate_semester_plans(completed_courses, interest_profile, course_count=2)
    for score, plan in plans:
        print(score, plan)









