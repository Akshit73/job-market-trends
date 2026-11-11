
import pandas as pd
import pytest
import requests

from src.extract import extract_jobs
from src.transform import transform_jobs
from src.load import load_jobs


# -------------------------
# EXTRACT TESTS
# -------------------------

def test_extract_maps_api_data(monkeypatch):
    api_job = {
        "id": 101,
        "title": "Python Developer",
        "organization": "TechCorp",
        "location": "Delhi",
        "country": "IN",
        "skillCategory": "Technology",
        "jobType": "Full-time",
        "category": "Technology",
        "salary": None,
        "descriptionExcerpt": "Python development role",
        "postedAt": "2026-11-01",
        "closingDate": None,
        "url": "https://example.com/job/101",
    }

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "jobs": [api_job],
                "meta": {"hasMore": False},
            }

    monkeypatch.setattr(
        "src.extract.requests.get",
        lambda *args, **kwargs: MockResponse()
    )

    result = extract_jobs()

    assert len(result) == 1
    assert result.iloc[0]["job_id"] == "101"
    assert result.iloc[0]["job_title"] == "Python Developer"
    assert result.iloc[0]["company"] == "TechCorp"
    assert result.iloc[0]["source"] == "Dev Global Jobs"


def test_extract_handles_pagination(monkeypatch):
    calls = []

    class MockResponse:
        def __init__(self, offset):
            self.offset = offset

        def raise_for_status(self):
            pass

        def json(self):
            job = {
                "id": self.offset + 1,
                "title": "Developer",
                "organization": "Company",
                "location": "Delhi",
                "country": "IN",
                "url": "https://example.com/job",
            }
            return {
                "jobs": [job],
                "meta": {
                    "hasMore": self.offset == 0
                },
            }

    def mock_get(url, params, timeout):
        calls.append(params["offset"])
        return MockResponse(params["offset"])

    monkeypatch.setattr("src.extract.requests.get", mock_get)

    result = extract_jobs()

    assert calls == [0, 1]
    assert len(result) == 2


def test_extract_handles_api_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Connection failed")

    monkeypatch.setattr("src.extract.requests.get", mock_get)

    with pytest.raises(RuntimeError, match="Could not fetch"):
        extract_jobs()


def test_extract_rejects_empty_response(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "jobs": [],
                "meta": {"hasMore": False},
            }

    monkeypatch.setattr(
        "src.extract.requests.get",
        lambda *args, **kwargs: MockResponse()
    )

    with pytest.raises(RuntimeError, match="no Indian job listings"):
        extract_jobs()


# -------------------------
# TRANSFORM TESTS
# -------------------------

def test_transform_removes_duplicate_job_ids():
    data = pd.DataFrame([
        {
            "job_id": "101",
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        },
        {
            "job_id": "101",
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        },
    ])

    result = transform_jobs(data)

    assert len(result) == 1


def test_transform_removes_missing_job_titles():
    data = pd.DataFrame([
        {
            "job_id": "101",
            "job_title": None,
            "company": "TechCorp",
            "location": "Delhi",
        },
        {
            "job_id": "102",
            "job_title": "Data Analyst",
            "company": "DataWorks",
            "location": "Delhi",
        },
    ])

    result = transform_jobs(data)

    assert len(result) == 1
    assert result.iloc[0]["job_title"] == "Data Analyst"


def test_transform_standardizes_location_and_country():
    data = pd.DataFrame([
        {
            "job_id": "101",
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "delhi",
            "country": "in",
        }
    ])

    result = transform_jobs(data)

    assert result.iloc[0]["location"] == "Delhi"
    assert result.iloc[0]["country"] == "IN"


# -------------------------
# LOAD TESTS
# -------------------------

@pytest.fixture
def sample_jobs():
    return pd.DataFrame([
        {
            "job_id": "101",
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        },
        {
            "job_id": "102",
            "job_title": "Data Analyst",
            "company": "DataWorks",
            "location": "Mumbai",
        },
    ])


def test_load_inserts_jobs_into_database(
    tmp_path, monkeypatch, sample_jobs
):
    monkeypatch.chdir(tmp_path)

    load_jobs(sample_jobs)

    import sqlite3

    conn = sqlite3.connect("data/jobs.db")

    count = conn.execute(
        "SELECT COUNT(*) FROM job_listings"
    ).fetchone()[0]

    conn.close()

    assert count == 2


def test_load_updates_existing_job_and_preserves_first_seen(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)

    import sqlite3

    original = pd.DataFrame([
        {
            "job_id": "101",
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        }
    ])

    load_jobs(original)

    conn = sqlite3.connect("data/jobs.db")

    first_seen_before = conn.execute(
        "SELECT first_seen FROM job_listings WHERE job_id = '101'"
    ).fetchone()[0]

    conn.close()

    updated = pd.DataFrame([
        {
            "job_id": "101",
            "job_title": "Senior Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        }
    ])

    load_jobs(updated)

    conn = sqlite3.connect("data/jobs.db")

    row = conn.execute("""
        SELECT job_title, first_seen
        FROM job_listings
        WHERE job_id = '101'
    """).fetchone()

    conn.close()

    assert row[0] == "Senior Python Developer"
    assert row[1] == first_seen_before


@pytest.mark.parametrize("invalid_id", [None, "", "   "])
def test_load_rejects_invalid_job_ids(
    tmp_path, monkeypatch, invalid_id
):
    monkeypatch.chdir(tmp_path)

    data = pd.DataFrame([
        {
            "job_id": invalid_id,
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        }
    ])

    with pytest.raises(ValueError, match="Job IDs cannot be empty"):
        load_jobs(data)


# -------------------------
# PIPELINE TEST
# -------------------------

def test_pipeline_runs_all_stages(monkeypatch):
    import src.pipeline as pipeline

    sample_data = pd.DataFrame([
        {
            "job_id": "101",
            "job_title": "Python Developer",
            "company": "TechCorp",
            "location": "Delhi",
        }
    ])

    calls = []

    monkeypatch.setattr(
        pipeline,
        "extract_jobs",
        lambda: calls.append("extract") or sample_data
    )

    monkeypatch.setattr(
        pipeline,
        "transform_jobs",
        lambda df: calls.append("transform") or df
    )

    monkeypatch.setattr(
        pipeline,
        "load_jobs",
        lambda df: calls.append("load")
    )

    result = pipeline.run_pipeline()

    assert calls == ["extract", "transform", "load"]
    assert len(result) == 1
