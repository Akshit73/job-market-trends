import sqlite3
from pathlib import Path


def load_jobs(df):
    """Load cleaned job listings into an SQLite database."""

    # Create the data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Connect to the database
    db_path = data_dir / "jobs.db"

    conn = sqlite3.connect(db_path)

    try:
        # Save the DataFrame into the database
        df.to_sql(
            "job_listings",
            conn,
            if_exists="replace",
            index=False
        )

        print(f"Successfully loaded {len(df)} jobs into the database.")

    finally:
        conn.close()


if __name__ == "__main__":
    from src.extract import extract_jobs
    from src.transform import transform_jobs

    jobs = extract_jobs()
    clean_jobs = transform_jobs(jobs)
    load_jobs(clean_jobs)