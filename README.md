# Job Market Intelligence

An India-focused job market analytics dashboard that collects job listings through an API, processes and stores the data using an ETL pipeline, and presents insights through interactive visualizations.

## Overview

Job Market Intelligence is a Python-based data analytics project designed to explore job market trends through structured job listing data.

The project follows an ETL (Extract, Transform, Load) architecture to collect job listings, clean and standardize the records, store them in an SQLite database, and visualize the results through an interactive Streamlit dashboard.

## Features

- Automated job listing extraction through the Dev Global Jobs API.
- Pagination support for retrieving job records.
- Data cleaning and transformation using Pandas.
- Duplicate job ID removal.
- Validation of API response structures and job records.
- SQLite database storage.
- Tracking of when job records were first and last observed.
- Interactive dashboard built with Streamlit.
- Job market analysis by location, company, job type and skill domain.
- Interactive visualizations using Plotly.
- Automated tests using Pytest.
- Continuous integration using GitHub Actions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and transformation |
| Requests | API integration |
| SQLite | Database storage |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| Pytest | Automated testing |
| Git & GitHub | Version control |
| GitHub Actions | Continuous integration |

## Project Architecture

The project follows an ETL architecture:

```text
             Dev Global Jobs API
                      |
                      v
               EXTRACT
              src/extract.py
                      |
                      v
              TRANSFORM
             src/transform.py
                      |
                      v
                 LOAD
               src/load.py
                      |
                      v
               SQLite DB
              data/jobs.db
                      |
                      v
             Streamlit Dashboard
                  app.py
                      |
                      v
             Interactive Analytics
```

## Project Structure

```text
job-market-trends/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── data/
│   └── jobs.db
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── tests/
│   └── test_pipeline.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Source

Job listing data is collected using the Dev Global Jobs API.

**Provider:** [Dev Global Jobs](https://devglobaljobs.com/)

**API endpoint:**
`https://devglobaljobs.com/api/v1/jobs`

The extractor requests India-focused job listings and supports pagination, with a maximum of five pages and ten records per page per extraction run.

The dashboard uses the records stored in the local SQLite database. Data availability depends on the API response and the last successful extraction.

## ETL Pipeline

### 1. Extract

File: `src/extract.py`

- Sends HTTP requests to the job listings API.
- Retrieves job records using pagination.
- Validates API response structures.
- Skips malformed records and records without valid job IDs.
- Removes duplicate job IDs.

### 2. Transform

File: `src/transform.py`

- Removes duplicate job listings.
- Handles missing essential information.
- Cleans text fields.
- Standardizes location formatting.
- Standardizes country codes.
- Converts salary values into numeric format where possible.

### 3. Load

File: `src/load.py`

- Stores processed records in SQLite.
- Uses job IDs to prevent duplicate records.
- Updates existing job records.
- Maintains `first_seen` and `last_seen` tracking fields.
- Uses database transactions for data integrity.

## Dashboard

The Streamlit dashboard provides an interactive overview of the collected job listings.

It includes:

- Total job listings.
- Companies represented in the dataset.
- Listed locations.
- Skill domains.
- Job distribution by location.
- Job distribution by skill domain.
- Employment type distribution.
- Top companies by listing count.
- Technical keyword analysis.
- Salary visualization when salary information is available.

## Installation and Setup

### Prerequisites

- Python 3.12 or later.
- Git.
- Internet connection for API extraction.

### 1. Clone the repository

```bash
git clone https://github.com/Akshit73/job-market-trends.git
```

### 2. Navigate to the project directory

```bash
cd job-market-trends
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment

For Linux:

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

### Run the ETL pipeline

```bash
python -m src.pipeline
```

This executes the extraction, transformation and loading stages.

### Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will normally be available at:

`http://localhost:8501`

## Automated Testing

The project uses Pytest to test the ETL pipeline.

Run the test suite:

```bash
python -m pytest -v
```

Tests cover:

- API response mapping.
- API pagination.
- API request failures.
- Empty API responses.
- Invalid API response structures.
- Malformed job records.
- Duplicate job removal.
- Missing essential information.
- Location and country standardization.
- Database insertion.
- Database updates.
- First-seen tracking.
- Invalid job ID handling.
- ETL pipeline execution order.

GitHub Actions automatically runs the tests on pushes and pull requests.

## Data Limitations

- Available records depend on the external API.
- Each extraction run retrieves a maximum of 50 records.
- Salary information may not be available for every listing.
- Experience requirements and individual skills may not be explicitly provided.
- Dashboard figures represent records available in the local database, not the entire Indian job market.
- The API's indexed listing count should not be interpreted as the number of active vacancies.

## Future Improvements

- Expand automated test coverage.
- Improve structured logging and error reporting.
- Add more detailed job market trend analysis.
- Improve historical data tracking.
- Introduce additional filtering and analytical capabilities.
- Expand data quality monitoring.

## Author
