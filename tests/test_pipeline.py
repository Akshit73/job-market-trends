import pandas as pd

from src.transform import transform_jobs


def test_duplicate_jobs_are_removed():
    data = pd.DataFrame([
        {
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
            "skills": "Python, SQL",
            "experience": "Entry Level",
        },
        {
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
            "skills": "Python, SQL",
            "experience": "Entry Level",
        },
    ])

    result = transform_jobs(data)

    assert len(result) == 1


def test_missing_job_titles_are_removed():
    data = pd.DataFrame([
        {
            "job_title": None,
            "company": "TechCorp",
            "location": "Delhi",
            "skills": "Python, SQL",
            "experience": "Entry Level",
        },
        {
            "job_title": "Data Analyst",
            "company": "DataWorks",
            "location": "Delhi",
            "skills": "Python, Excel",
            "experience": "Entry Level",
        },
    ])

    result = transform_jobs(data)

    assert len(result) == 1
    assert result.iloc[0]["job_title"] == "Data Analyst"


def test_location_is_standardized():
    data = pd.DataFrame([
        {
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "delhi",
            "skills": "Python, SQL",
            "experience": "Entry Level",
        },
    ])

    result = transform_jobs(data)

    assert result.iloc[0]["location"] == "Delhi"