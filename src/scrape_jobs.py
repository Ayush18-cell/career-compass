import requests
from bs4 import BeautifulSoup
import pandas as pd

jobs = []

url = "https://example-job-site.com/jobs?q=data+analyst"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

for job in soup.find_all("div", class_="job-card"):
    title = job.find("h2").text.strip()
    skills = job.find("span", class_="skills").text.strip()
    salary = job.find("span", class_="salary").text.strip()
    experience = job.find("span", class_="experience").text.strip()

    jobs.append([title, skills, experience, salary])

df = pd.DataFrame(jobs, columns=["title", "skills", "experience", "salary"])
df.to_csv("data/raw_jobs.csv", index=False)
