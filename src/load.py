
import sqlite3
from pathlib import Path
import pandas as pd


def load_jobs(df):
    """Load jobs into SQLite without deleting existing records."""

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    db_path = data_dir / "jobs.db"

    df = df.copy()

    if "job_id" not in df.columns:
        raise ValueError("Missing job_id column.")

    if (
       df["job_id"].isna().any()
       or df["job_id"].astype(str).str.strip().eq("").any()
    ):
       raise ValueError("Job IDs cannot be empty.")

    df["job_id"] = df["job_id"].astype(str)

    df = df.drop_duplicates(subset=["job_id"], keep="last")

    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()

        # Create table if it does not exist.
        df.head(0).to_sql(
            "job_listings",
            conn,
            if_exists="append",
            index=False
        )

        # Add tracking columns.
        existing_columns = {
            row[1]
            for row in cursor.execute(
                "PRAGMA table_info(job_listings)"
            ).fetchall()
        }

        if "first_seen" not in existing_columns:
            cursor.execute(
                "ALTER TABLE job_listings "
                "ADD COLUMN first_seen TEXT"
            )

        if "last_seen" not in existing_columns:
            cursor.execute(
                "ALTER TABLE job_listings "
                "ADD COLUMN last_seen TEXT"
            )

        # Remove old duplicate IDs before creating unique index.
        cursor.execute("""
            DELETE FROM job_listings
            WHERE rowid NOT IN (
                SELECT MAX(rowid)
                FROM job_listings
                GROUP BY job_id
            )
        """)

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_job_listings_job_id
            ON job_listings(job_id)
        """)

        # Find columns available in the database.
        db_columns = {
            row[1]
            for row in cursor.execute(
                "PRAGMA table_info(job_listings)"
            ).fetchall()
        }

        incoming_columns = [
            column for column in df.columns
            if column in db_columns
        ]

        quoted_columns = [
            f'"{column}"' for column in incoming_columns
        ]

        placeholders = ", ".join(
            ["?"] * len(incoming_columns)
        )

        update_columns = [
            column for column in incoming_columns
            if column != "job_id"
        ]

        update_statement = ", ".join(
            f'"{column}" = excluded."{column}"'
            for column in update_columns
        )

        sql = f"""
            INSERT INTO job_listings (
                {", ".join(quoted_columns)},
                first_seen,
                last_seen
            )
            VALUES (
                {placeholders},
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT(job_id) DO UPDATE SET
            {update_statement},
            first_seen = COALESCE(
                     job_listings.first_seen,
                     CURRENT_TIMESTAMP
        ),
            last_seen = CURRENT_TIMESTAMP
        """

        records = []


        for row in df[incoming_columns].itertuples(
            index=False,
            name=None
        ):
            records.append(tuple(
                None if pd.isna(value) else value
                for value in row
            ))

        cursor.executemany(sql, records)

        conn.commit()

        total_jobs = cursor.execute(
            "SELECT COUNT(*) FROM job_listings"
        ).fetchone()[0]

        print(f"Successfully processed {len(df)} jobs.")
        print(f"Total unique jobs in database: {total_jobs}")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    from src.extract import extract_jobs
    from src.transform import transform_jobs

    jobs = extract_jobs()
    clean_jobs = transform_jobs(jobs)
    load_jobs(clean_jobs)
