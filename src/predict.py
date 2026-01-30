import joblib

# Load model and skill list (normalize skill names)
model = joblib.load("salary_model.pkl")
skills_list = [s.strip() for s in joblib.load("skills.pkl")]


def predict_salary(candidate_skills):
    """Predict salary and return top missing skills.

    candidate_skills: list of skill strings (assumed already lowercased/stripped)
    """
    candidate_skills = [s.strip() for s in candidate_skills]
    input_vector = [1 if skill in candidate_skills else 0 for skill in skills_list]
    salary = model.predict([input_vector])

    missing_skills = [s for s in skills_list if s not in candidate_skills]

    return float(salary[0]), missing_skills[:5]


if __name__ == "__main__":
    # simple local test
    salary, gaps = predict_salary(["python", "sql", "excel"])
    print("Predicted Salary (LPA):", salary)
    print("Suggested Skills to Learn:", gaps)
