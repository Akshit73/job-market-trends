
import pandas as pd


def transform_jobs(df):
    """Clean and transform Indian job listing data."""

    df = df.copy()

    # Step 1: Remove duplicate listings using unique job IDs
    if "job_id" in df.columns:
        df = df.drop_duplicates(subset=["job_id"], keep="first")
    else:
        df = df.drop_duplicates()

    # Step 2: Handle missing essential information
    essential_columns = ["job_title", "company", "location"]

    df = df.dropna(subset=essential_columns)

    for column in essential_columns:
        df = df[df[column].astype(str).str.strip() != ""]

    # Step 3: Clean text columns safely
    text_columns = [
        "job_title",
        "company",
        "location",
        "skills",
        "experience",
        "job_type",
        "category",
        "description",
        "source",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .fillna("Not specified")
                .astype(str)
                .str.strip()
            )

    # Step 4: Standardize location formatting
    if "location" in df.columns:
        df["location"] = df["location"].str.title()

    # Step 5: Standardize country codes
    if "country" in df.columns:
        df["country"] = df["country"].str.upper()

    # Step 6: Convert salary values to numeric where possible
    if "salary" in df.columns:
        df["salary"] = pd.to_numeric(
            df["salary"], errors="coerce"
        )

    # Step 7: Remove duplicate application URLs
    if "job_url" in df.columns:
        df = df.drop_duplicates(subset=["job_id"], keep="first")

    # Step 8: Reset index
    df = df.reset_index(drop=True)

    print(f"Transformed data: {len(df)} job listings.")

    return df
