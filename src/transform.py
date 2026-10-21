import pandas as pd


def transform_jobs(df):
    """Clean and transform job listing data."""

    # Step 1: Remove duplicate job listings
    df = df.drop_duplicates()

    # Step 2: Remove rows with missing essential information
    df = df.dropna(subset=["job_title", "company", "location"])

    # Step 3: Remove extra spaces from text columns
    columns = ["job_title", "company", "location", "skills", "experience"]

    for column in columns:
        df[column] = df[column].str.strip()

    # Step 4: Standardize location names
    df["location"] = df["location"].str.title()

    # Step 5: Reset the row numbering
    df = df.reset_index(drop=True)

    print(f"Transformed data: {len(df)} job listings.")

    return df