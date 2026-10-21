from src.extract import extract_jobs
from src.transform import transform_jobs
from src.load import load_jobs


def run_pipeline():
    # Step 1: Extract
    jobs = extract_jobs()

    # Step 2: Transform
    clean_jobs = transform_jobs(jobs)

    # Step 3: Load
    load_jobs(clean_jobs)

    print("\nETL pipeline completed successfully!")

    return clean_jobs


if __name__ == "__main__":
    run_pipeline()