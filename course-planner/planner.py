import json
from itertools import combinations

def load_courses():
    with open("data/courses.json", "r") as f:
        return json.load(f)

courses = load_courses()

def prereqs_met(course_name, completed):
    return all(prereq in completed for prereq in courses[course_name]["prereqs"])
  
def valid_schedule(schedule, min_units=8, max_units=12):
    total_units = 0
    times = set()
    for course_name in schedule:
        course = courses[course_name]
        total_units += course["units"]
    return min_units <= total_units <= max_units
  
def offered_in_term(course, term):
    return term in course["terms_offered"]
def Fall(course):
  if not offered_in_term(course, "Fall"):
    return False
  else:
    return True
def Spring(course):
  if not offered_in_term(course, "Spring"):
    return False
  else:
    return True

def interest_alignment(schedule, interest_profile):
    score = 0
    for course_name in schedule:
        topics = courses[course_name]["topics"]
        for t in topics:
            score += interest_profile.get(t, 0)
    return score / len(schedule)

def workload_balance(schedule):
    avg = sum(courses[c]["workload"] for c in schedule) / len(schedule)
    return 1 - abs(avg - 0.6)  # prefer moderate workload

def major_progress(schedule):
    return sum(
        1 for c in schedule if courses[c].get("major_required", False)
    ) / len(schedule)

def score_semester(courses, interest_profile, weights):
    score = 0.0
    for c in courses:
        for t in c.get("topics", []):
            score += interest_profile.get(t, 0) * weights["interest"]
        score -= c["difficulty"] * weights["difficulty"]
        score += c["professor_rating"] * weights["rating"]
    return score

def generate_semester_plans(
    completed,
    interest_profile,
    course_count=3,
    weights= None,
):
    if weights is None:
        weights = {
            "interest": 0.4,
            "workload": 0.3,
            "major": 0.3,
        }

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

    interest_profile = {
        "genomics": 1.0,
        "statistics": 0.9,
        "programming": 0.8,
        "wet_lab": 0.5,
    }

    top_plans = generate_semester_plans(
        completed_courses,
        interest_profile,
        course_count=3,
    )

    for i, (score, plan) in enumerate(top_plans, 1):
        print(f"Plan {i} | Score: {round(score, 3)}")
        for c in plan:
            print("  -", c)
        print()










