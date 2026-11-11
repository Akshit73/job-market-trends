import requests
import pandas as pd
from datetime import datetime, timezone


API_URL = "https://devglobaljobs.com/api/v1/jobs"

PAGE_SIZE = 10
MAX_PAGES = 5


def extract_jobs():
    """Fetch Indian job listings from the Dev Global Jobs API."""

    print("Fetching Indian job listings from Dev Global Jobs...")

    records = []
    offset = 0

    try:
        for page in range(MAX_PAGES):

            response = requests.get(
                API_URL,
                params={
                    "country": "in",
                    "limit": PAGE_SIZE,
                    "offset": offset,
                },
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            # Validate API response structure.
            if not isinstance(data, dict):
                raise RuntimeError(
                    "Invalid API response: expected a JSON object."
                )

            jobs = data.get("jobs", [])
            metadata = data.get("meta", {})

            if not isinstance(jobs, list):
                raise RuntimeError(
                    "Invalid API response: jobs must be a list."
                )

            if not isinstance(metadata, dict):
                raise RuntimeError(
                    "Invalid API response: meta must be an object."
                )

            if not jobs:
                break

            # Process individual job records.
            for job in jobs:

                # Skip malformed records.
                if not isinstance(job, dict):
                    continue

                job_id = job.get("id")

                # Skip records without valid IDs.
                if job_id is None or str(job_id).strip() == "":
                    continue

                records.append({
                    "job_id": str(job_id).strip(),
                    "job_title": job.get("title", ""),
                    "company": job.get("organization", ""),
                    "location": job.get("location", "Not specified"),
                    "country": job.get("country", ""),
                    "skills": "Not provided",
                    "skill_category": job.get(
                        "skillCategory", "Not specified"
                    ),
                    "experience": "Not specified",
                    "job_type": job.get(
                        "jobType", "Not specified"
                    ),
                    "category": job.get(
                        "category", "Not specified"
                    ),
                    "salary": job.get("salary"),
                    "description": job.get(
                        "descriptionExcerpt", ""
                    ),
                    "posted_date": job.get("postedAt", ""),
                    "closing_date": job.get("closingDate"),
                    "job_url": job.get("url", ""),
                    "source": "Dev Global Jobs",
                    "extracted_at": datetime.now(
                        timezone.utc
                    ).isoformat(),
                })

            # Pagination.
            offset += len(jobs)

            if not metadata.get("hasMore", False):
                break

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not fetch job listings: {error}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            f"Invalid JSON received from API: {error}"
        ) from error

    if not records:
        raise RuntimeError(
          "The API returned no Indian job listings (no valid records)."
        )

    df = pd.DataFrame(records)

    # Remove duplicate job IDs.
    df = df.drop_duplicates(subset=["job_id"])

    print(
        f"Successfully extracted {len(df)} Indian job listings."
    )

    print("Source: Dev Global Jobs")
    print("Country: India")

    return df


if __name__ == "__main__":

    jobs_df = extract_jobs()

    print("\nSample listings:")

    print(
        jobs_df[
            [
                "job_title",
                "company",
                "location",
                "job_type",
                "job_url",
            ]
        ].head(10).to_string(index=False)
    )