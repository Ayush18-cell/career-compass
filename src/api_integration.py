"""
Real Job Data Integration Module
Demonstrates how to fetch job data from Indeed, LinkedIn, and Glassdoor APIs.
"""

import requests
import pandas as pd
from typing import List, Dict
import os
from datetime import datetime

# Configuration for API keys (set via environment variables)
INDEED_API_KEY = os.getenv("INDEED_API_KEY")
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
GLASSDOOR_API_KEY = os.getenv("GLASSDOOR_API_KEY")

class JobDataCollector:
    """Fetch job data from multiple sources."""
    
    @staticmethod
    def fetch_from_indeed(keywords: str, location: str = "India") -> List[Dict]:
        """
        Fetch jobs from Indeed API.
        
        Requires: Indeed API key from https://opensource.indeedeng.io/api-portal/
        """
        if not INDEED_API_KEY:
            print("⚠ Indeed API key not configured. Set INDEED_API_KEY environment variable.")
            return []
        
        url = "https://api.indeed.com/ads/apisearch"
        params = {
            "publisher": INDEED_API_KEY,
            "q": keywords,
            "l": location,
            "format": "json",
            "limit": 100,
            "sort": "date"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for job in data.get("results", []):
                jobs.append({
                    "title": job.get("jobtitle"),
                    "company": job.get("company"),
                    "location": job.get("formattedLocationFull"),
                    "skills": job.get("snippet", ""),  # Parse from snippet
                    "salary": job.get("salary", ""),
                    "source": "Indeed"
                })
            return jobs
        except Exception as e:
            print(f"Error fetching from Indeed: {e}")
            return []
    
    @staticmethod
    def fetch_from_linkedin(keywords: str, location: str = "India") -> List[Dict]:
        """
        Fetch jobs from LinkedIn API (requires RapidAPI integration).
        
        Setup: Install via pip: pip install linkedin-api
        Then use: from linkedin_api import Linkedin
        """
        if not LINKEDIN_API_KEY:
            print("⚠ LinkedIn API key not configured. Use RapidAPI LinkedIn Jobs API.")
            return []
        
        # Example using RapidAPI LinkedIn endpoint
        url = "https://linkedin-api1.p.rapidapi.com/search"
        headers = {
            "x-rapidapi-key": LINKEDIN_API_KEY,
            "x-rapidapi-host": "linkedin-api1.p.rapidapi.com"
        }
        params = {
            "keywords": keywords,
            "locationId": "IN",  # India
            "limit": 100
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for job in data.get("jobs", []):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("companyName"),
                    "location": job.get("location"),
                    "skills": job.get("description", ""),
                    "salary": "",
                    "source": "LinkedIn"
                })
            return jobs
        except Exception as e:
            print(f"Error fetching from LinkedIn: {e}")
            return []
    
    @staticmethod
    def fetch_from_glassdoor(keywords: str, location: str = "India") -> List[Dict]:
        """
        Fetch jobs from Glassdoor API.
        
        Setup: https://www.glassdoor.com/api
        """
        if not GLASSDOOR_API_KEY:
            print("⚠ Glassdoor API not available. Use web scraping (with robots.txt compliance).")
            return []
        
        print("Glassdoor API integration requires direct partnerships.")
        return []
    
    @staticmethod
    def collect_all_jobs(keywords: str, location: str = "India") -> pd.DataFrame:
        """Aggregate job data from all sources."""
        all_jobs = []
        
        print(f"\n📊 Collecting job data for: {keywords} in {location}")
        print("=" * 60)
        
        # Fetch from Indeed
        print("📍 Fetching from Indeed...")
        indeed_jobs = JobDataCollector.fetch_from_indeed(keywords, location)
        all_jobs.extend(indeed_jobs)
        print(f"   ✓ Found {len(indeed_jobs)} jobs")
        
        # Fetch from LinkedIn
        print("📍 Fetching from LinkedIn...")
        linkedin_jobs = JobDataCollector.fetch_from_linkedin(keywords, location)
        all_jobs.extend(linkedin_jobs)
        print(f"   ✓ Found {len(linkedin_jobs)} jobs")
        
        print("=" * 60)
        print(f"\n✓ Total jobs collected: {len(all_jobs)}")
        
        return pd.DataFrame(all_jobs) if all_jobs else pd.DataFrame()

def extract_skills_from_description(description: str) -> str:
    """
    Extract tech skills from job description using NLP.
    
    Common skills to match:
    """
    COMMON_SKILLS = [
        "Python", "Java", "JavaScript", "SQL", "C++",
        "React", "Django", "Flask", "Spring Boot", "Node.js",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "Pandas", "NumPy", "Scikit-learn",
        "Git", "Jenkins", "CI/CD", "Terraform"
    ]
    
    found_skills = []
    desc_lower = description.lower()
    for skill in COMMON_SKILLS:
        if skill.lower() in desc_lower:
            found_skills.append(skill)
    
    return ", ".join(found_skills) if found_skills else ""

if __name__ == "__main__":
    # Example: Collect data analyst jobs
    print("\n" + "=" * 60)
    print("Job Data Integration Example")
    print("=" * 60)
    
    print("\n📝 SETUP INSTRUCTIONS:")
    print("-" * 60)
    print("1. Indeed API:")
    print("   - Get key: https://opensource.indeedeng.io/api-portal/")
    print("   - Set: export INDEED_API_KEY='your_key'")
    print()
    print("2. LinkedIn API (via RapidAPI):")
    print("   - Sign up: https://rapidapi.com/")
    print("   - Find: 'LinkedIn API' on RapidAPI")
    print("   - Set: export LINKEDIN_API_KEY='your_key'")
    print()
    print("3. Glassdoor:")
    print("   - Requires business partnership")
    print("   - Alternative: Use web scraping (Selenium/BeautifulSoup)")
    print("-" * 60)
    
    # Simulate collection (will show warnings if keys not set)
    # df = JobDataCollector.collect_all_jobs("Data Analyst", "India")
    # if not df.empty:
    #     df.to_csv("data/collected_jobs.csv", index=False)
