
import pandas as pd
import re

df = pd.read_csv("data/raw_jobs.csv")

def extract_salary(salary):
    numbers = re.findall(r'\d+', salary)
    if len(numbers) >= 2:
        return (int(numbers[0]) + int(numbers[1])) / 2
    return None

df["salary_lpa"] = df["salary"].apply(extract_salary)
df.dropna(inplace=True)

df.to_csv("data/cleaned_jobs.csv", index=False)
