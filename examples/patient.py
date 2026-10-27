# Notebook: The patient. Keep its bugs for the agent to diagnose.
BUGGY_CODE = '''
def letter_grade(score):
    """Return the letter grade: 90+ is A, 80-89 is B, 70-79 is C, below 70 is F."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score > 70:
        return "C"
    else:
        return "F"


def class_report(students):
    """
    students: dict of name -> list of scores.
    Returns (report, topper):
      report: dict of name -> (average rounded to 1 decimal, letter grade).
              Students with no scores get (None, "N/A").
      topper: name of the student with the highest average.
    """
    report = {}
    for name, scores in students.items():
        avg = sum(scores) / len(score)
        report[name] = (round(avg, 1), letter_grade(avg))
    topper = max(report, key=lambda n: report[n][1])
    return report, topper


def class_average(students):
    """Return the average of every individual score in the class."""
    all_scores = [s for scores in students.values() for s in scores]
    return sum(all_scores) / len(students)


students = {
    "Asha": [92, 88, 95],
    "Ravi": [70, 72, 68],
    "Meera": [85, 79, 90],
    "Kabir": [],
}

report, topper = class_report(students)
for name, (avg, grade) in report.items():
    print(f"{name}: {avg} ({grade})")
print("Topper:", topper)
print("Class average:", round(class_average(students), 2))
'''
