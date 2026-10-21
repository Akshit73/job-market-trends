import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# Page configuration
st.set_page_config(
    page_title="Job Market Trends",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Job Market Trends Analysis")
st.caption("Explore job listings, hiring patterns, and in-demand skills.")

# Database path
DB_PATH = Path(__file__).parent / "data" / "jobs.db"


@st.cache_data
def load_data():
    """Read job listings from the SQLite database."""

    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM job_listings",
            conn,
        )


df = load_data()

if df.empty:
    st.warning("No job listings found. Run the ETL pipeline first.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

locations = sorted(df["location"].dropna().unique())

selected_locations = st.sidebar.multiselect(
    "Select locations",
    locations,
    default=locations,
)

roles = sorted(df["job_title"].dropna().unique())

selected_roles = st.sidebar.multiselect(
    "Select job roles",
    roles,
    default=roles,
)

filtered_df = df[
    df["location"].isin(selected_locations)
    & df["job_title"].isin(selected_roles)
].copy()

# Key metrics
st.subheader("Market Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Job Listings", len(filtered_df))
col2.metric("Companies", filtered_df["company"].nunique())
col3.metric("Locations", filtered_df["location"].nunique())

if filtered_df.empty:
    st.info("No jobs match your selected filters.")
    st.stop()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Jobs by Location")

    location_counts = (
        filtered_df["location"]
        .value_counts()
        .rename_axis("Location")
        .reset_index(name="Job Listings")
    )

    fig_location = px.bar(
        location_counts,
        x="Location",
        y="Job Listings",
        title="Job Listings Across Locations",
    )

    st.plotly_chart(fig_location, use_container_width=True)

with right:
    st.subheader("Popular Job Roles")

    role_counts = (
        filtered_df["job_title"]
        .value_counts()
        .rename_axis("Job Role")
        .reset_index(name="Job Listings")
    )

    fig_roles = px.bar(
        role_counts,
        x="Job Listings",
        y="Job Role",
        orientation="h",
        title="Job Listings by Role",
    )

    st.plotly_chart(fig_roles, use_container_width=True)

# Skills analysis
st.subheader("In-Demand Technical Skills")

skill_counts = {}

for skills in filtered_df["skills"].dropna():
    for skill in skills.split(","):
        skill = skill.strip()

        if skill:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

if skill_counts:
    skills_df = pd.DataFrame(
        skill_counts.items(),
        columns=["Skill", "Job Listings"],
    ).sort_values("Job Listings", ascending=False)

    fig_skills = px.bar(
        skills_df.head(10),
        x="Skill",
        y="Job Listings",
        title="Top 10 Skills in the Selected Listings",
    )

    st.plotly_chart(fig_skills, use_container_width=True)

# Job listings table
st.subheader("Job Listings")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Prototype using fictional sample data. "
    "These records do not represent verified live vacancies."
)