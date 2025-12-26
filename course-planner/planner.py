import json
from itertools import combinations

def load_courses():
    with open("data/courses.json", "r") as f:
        return json.load(f)

courses = load_courses()

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
        for t in topics:
            score += interest_profile.get(t, 0)
    return score / len(schedule)

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
    
def score_schedule(courses, interest_profile, weights):
    score = 0.0
    for c in courses:
        for t in c.get("topics", []):
            score += interest_profile.get(t, 0) * weights["interest"]
        score -= c["difficulty"] * weights["difficulty"]
        score += c["professor_rating"] * weights["rating"]
    return score
    
    eligible = [
        c for c in courses
        if prereqs_met(c, completed)
    ]
    
    plans = []
    for combo in combinations(eligible, course_count):
        if valid_schedule(combo):
            score = score_schedule(combo, interest_profile, weights)
            plans.append((score, combo))

    plans.sort(reverse=True, key=lambda x: x[0])
    return plans[:5]

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









