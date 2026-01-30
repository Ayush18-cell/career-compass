"""Generate synthetic job dataset with 500+ records for model training."""

import pandas as pd
import numpy as np
import random

# Define realistic job market data
ROLES = [
    # Technical Roles
    "Data Analyst", "Data Scientist", "Machine Learning Engineer",
    "Backend Developer", "Frontend Developer", "Full Stack Developer",
    "Data Engineer", "Cloud Engineer", "DevOps Engineer",
    "BI Analyst", "Software Engineer", "Business Analyst",
    "Analytics Consultant", "Junior Developer", "Senior Engineer",
    "Solutions Architect", "Technical Lead", "Engineering Manager",
    # MBA & Management Roles
    "Product Manager", "Project Manager", "Business Manager",
    "Operations Manager", "Strategy Consultant", "Management Consultant",
    "Finance Manager", "Business Analyst Manager", "Product Lead",
    "Scrum Master", "Agile Coach", "Program Manager"
]

SKILLS_BY_ROLE = {
    # Technical Roles
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI", "Tableau", "Statistics"],
    "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics", "TensorFlow", "Deep Learning"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "AWS", "GCP"],
    "Backend Developer": ["Python", "Java", "SQL", "REST API", "Django", "Spring Boot", "Node.js"],
    "Frontend Developer": ["JavaScript", "React", "CSS", "HTML", "Vue.js", "Angular"],
    "Full Stack Developer": ["Python", "JavaScript", "React", "SQL", "REST API", "Docker"],
    "Data Engineer": ["Python", "SQL", "Spark", "AWS", "ETL", "Hadoop", "Kafka"],
    "Cloud Engineer": ["AWS", "GCP", "Azure", "Kubernetes", "Docker", "Terraform"],
    "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "CI/CD", "Jenkins", "Git", "Linux"],
    "BI Analyst": ["SQL", "Power BI", "Tableau", "Excel", "Data Visualization"],
    "Software Engineer": ["Java", "SQL", "OOPs", "DSA", "REST API", "Microservices"],
    "Business Analyst": ["SQL", "Excel", "Power BI", "Communication", "Tableau"],
    "Analytics Consultant": ["Python", "SQL", "Power BI", "Statistics", "Communication"],
    # MBA & Management Roles
    "Product Manager": ["Product Strategy", "User Research", "Data Analysis", "Market Analysis", "Leadership"],
    "Project Manager": ["Project Management", "Agile", "Leadership", "Communication", "Risk Management"],
    "Business Manager": ["Business Strategy", "P&L Management", "Leadership", "Analytics", "Negotiation"],
    "Operations Manager": ["Operations", "Process Optimization", "Analytics", "Leadership", "Supply Chain"],
    "Strategy Consultant": ["Business Strategy", "Market Analysis", "Financial Analysis", "Consulting", "Research"],
    "Management Consultant": ["Consulting", "Problem Solving", "Data Analysis", "Leadership", "Communication"],
    "Finance Manager": ["Financial Analysis", "Budgeting", "Excel", "Accounting", "Risk Management"],
    "Business Analyst Manager": ["SQL", "Excel", "Power BI", "Leadership", "Agile"],
    "Product Lead": ["Product Strategy", "User Research", "Data Analysis", "Leadership", "Communication"],
    "Scrum Master": ["Agile", "Leadership", "Communication", "Project Management", "Mentoring"],
    "Agile Coach": ["Agile", "Coaching", "Leadership", "Training", "Process Optimization"],
    "Program Manager": ["Program Management", "Leadership", "Planning", "Communication", "Stakeholder Management"],
}

EXPERIENCE_LEVELS = ["0-1 year", "1-3 years", "2-5 years", "3-7 years", "5+ years"]

# Salary ranges by experience level (LPA)
SALARY_RANGES = {
    "0-1 year": (3, 6),
    "1-3 years": (5, 10),
    "2-5 years": (7, 15),
    "3-7 years": (10, 20),
    "5+ years": (15, 30),
}

# Certifications by role
CERTIFICATIONS_BY_ROLE = {
    # MBA Certifications
    "Product Manager": ["MBA", "PSPO", "CSPM"],
    "Project Manager": ["MBA", "PMP", "CAPM", "PRINCE2"],
    "Business Manager": ["MBA", "CHRL"],
    "Operations Manager": ["MBA", "APICS", "Six Sigma"],
    "Strategy Consultant": ["MBA", "Strategic Management Cert"],
    "Management Consultant": ["MBA", "MCSE"],
    "Finance Manager": ["MBA", "CFA", "CA"],
    "Business Analyst Manager": ["MBA", "CBAP", "CCBA"],
    "Product Lead": ["MBA", "PSPO"],
    "Scrum Master": ["CSM", "PSM", "CSPO"],
    "Agile Coach": ["CAL", "PMC", "CSM"],
    "Program Manager": ["PgMP", "MBA", "SAFe"],
    # Technical Certifications
    "Data Scientist": ["Azure Data Scientist", "GCP ML Engineer", "AWS ML"],
    "Machine Learning Engineer": ["TensorFlow Cert", "AWS ML", "Azure ML"],
    "Cloud Engineer": ["AWS Solutions Architect", "AZ-305", "GCP Associate"],
    "DevOps Engineer": ["AWS DevOps", "Kubernetes (CKA)", "Jenkins"],
    "Backend Developer": ["AWS Developer", "Spring Professional"],
    "Data Analyst": ["Google Data Analytics", "Tableau Specialist", "Power BI Analyst"],
}

def generate_skills(role, num_skills=4, premium_skills=None):
    """Generate skill set for a role with optional premium skills."""
    if premium_skills is None:
        premium_skills = []
    available = SKILLS_BY_ROLE.get(role, ["Python", "SQL"])
    selected = list(premium_skills)
    remaining = [s for s in available if s not in selected]
    selected.extend(random.sample(remaining, min(num_skills - len(selected), len(remaining))))
    return ", ".join(selected)

def generate_salary(experience, premium_skill_count=0):
    """Generate salary based on experience level and premium skills."""
    low, high = SALARY_RANGES.get(experience, (3, 6))
    base_salary = np.random.uniform(low, high)
    # Boost salary for premium skills (ML, Cloud, etc.)
    premium_boost = premium_skill_count * 0.5
    return round(base_salary + premium_boost, 1)

PREMIUM_SKILLS = ["Machine Learning", "Deep Learning", "AWS", "GCP", "Azure", "Kubernetes", "Spark"]

def get_certifications(role):
    """Get recommended certifications for a role."""
    certs = CERTIFICATIONS_BY_ROLE.get(role, [])
    if certs:
        num_certs = random.randint(1, min(2, len(certs)))
        return ", ".join(random.sample(certs, num_certs))
    return ""

def generate_dataset(n_records=500):
    """Generate synthetic job dataset with skill-salary correlation and certifications."""
    data = []
    for _ in range(n_records):
        role = random.choice(ROLES)
        exp = random.choice(EXPERIENCE_LEVELS)
        
        # 30% chance of including a premium skill (which boosts salary)
        premium_count = 1 if random.random() < 0.3 else 0
        premium_skills = random.sample(PREMIUM_SKILLS, premium_count) if premium_count > 0 else []
        
        # MBA roles get higher salary bonus
        mba_bonus = 2 if any(mba_role in role for mba_role in ["Manager", "Consultant", "Product", "Scrum", "Agile"]) else 0
        
        skills = generate_skills(role, premium_skills=premium_skills)
        salary = generate_salary(exp, premium_skill_count=premium_count)
        salary = round(salary + mba_bonus, 1)  # Add MBA bonus
        certifications = get_certifications(role)
        
        data.append({
            "title": role,
            "skills": skills,
            "experience": exp,
            "salary_lpa": salary,
            "certifications": certifications
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    print(f"Generating {500} synthetic job records...")
    df = generate_dataset(500)
    
    df.to_csv("data/cleaned_jobs.csv", index=False)
    print(f"\n✓ Saved {len(df)} records to data/cleaned_jobs.csv")
    print(f"\nDataset preview:")
    print(df.head(10))
    print(f"\nSalary statistics (LPA):")
    print(df["salary_lpa"].describe())
