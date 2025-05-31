import streamlit as st
import pandas as pd

# Load CSV data
df = pd.read_csv("universities_courses.csv")

st.title("🎓 German University Course Finder")

# Tuition filter
tuition_filter = st.selectbox("Tuition", ["All", "Free only", "Paid only"])
if tuition_filter == "Free only":
    df = df[df["tuition_eur"] == 0]
elif tuition_filter == "Paid only":
    df = df[df["tuition_eur"] > 0]

# Language filter
language = st.selectbox("Language", ["All"] + sorted(df["language"].unique()))
if language != "All":
    df = df[df["language"] == language]

# Location filter
location = st.selectbox("Location", ["All"] + sorted(df["location"].unique()))
if location != "All":
    df = df[df["location"] == location]

# Degree type filter
degree = st.selectbox("Degree", ["All"] + sorted(df["degree_type"].unique()))
if degree != "All":
    df = df[df["degree_type"] == degree]

# Show results
st.subheader(f"📚 Found {len(df)} matching courses")
st.dataframe(df)

# Download button
st.download_button("📥 Download CSV", df.to_csv(index=False), "filtered_courses.csv")