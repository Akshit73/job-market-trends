import pandas as pd


def extract_jobs():
    """Extract job listings from a sample dataset."""

    jobs = [
        {
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
            "skills": "Python, SQL, Pandas",
            "experience": "Entry Level",
        },
        {
            "job_title": "Data Analyst",
            "company": "DataWorks",
            "location": "Bangalore",
            "skills": "Python, SQL, Excel",
            "experience": "Entry Level",
        },
        {
            "job_title": "Software Engineer",
            "company": "InnovateTech",
            "location": "Delhi",
            "skills": "Python, Java, SQL",
            "experience": "Entry Level",
        },
        {
            "job_title": "Data Scientist",
            "company": "AI Solutions",
            "location": "Mumbai",
            "skills": "Python, Machine Learning, Pandas",
            "experience": "Mid Level",
        },
        {
            "job_title": "Web Developer",
            "company": "WebWorks",
            "location": "Bangalore",
            "skills": "HTML, CSS, JavaScript",
            "experience": "Entry Level",
        },
        {
            "job_title": "Python Developer",
            "company": "CloudTech",
            "location": "Mumbai",
            "skills": "Python, Django, SQL",
            "experience": "Mid Level",
        },
        {
            "job_title": "Data Analyst",
            "company": "AnalyticsPro",
            "location": "Delhi",
            "skills": "SQL, Excel, Power BI",
            "experience": "Entry Level",
        },
        {
            "job_title": "DevOps Engineer",
            "company": "CloudTech",
            "location": "Bangalore",
            "skills": "Linux, Docker, AWS",
            "experience": "Mid Level",
        },
    ]

    df = pd.DataFrame(jobs)

    print(f"Extracted {len(df)} job listings.")

    return df


if __name__ == "__main__":
    jobs_df = extract_jobs()
    print(jobs_df)