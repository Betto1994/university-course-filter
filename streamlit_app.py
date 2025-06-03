import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="University Course Explorer", layout="wide")
st.title("🎓 University Course Explorer in Germany")

file_path = "universities_courses.xlsx"

if os.path.exists(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name="Data base")
        st.success("✅ Excel file loaded successfully.")

        with st.expander("🔍 Preview Dataset"):
            st.dataframe(df)

        # Sidebar Filters
        st.sidebar.header("📊 Filter Options")

        # Tuition Fees Filter
        fee_filter = st.sidebar.selectbox("💰 Tuition Fees", options=["All", "Free", "Paid"])
        if fee_filter == "Free":
            df = df[df["Tuition Fees"].str.upper() == "N"]
        elif fee_filter == "Paid":
            df = df[df["Tuition Fees"].str.upper() == "Y"]

        # Intake Semester Filter
        if "Intake Semester" in df.columns:
            intake_options = ["All", "Winter", "Summer", "Winter and summer"]
            intake_filter = st.sidebar.selectbox("📅 Intake Semester", intake_options)
            if intake_filter != "All":
                df = df[df["Intake Semester"].str.lower() == intake_filter.lower()]

        # Application Fees Filter (moved to sidebar)
        app_fee_filter = st.sidebar.selectbox("💸 Application Fees", ["All", "Yes", "No", "Blank"])
        if app_fee_filter == "Yes":
            df = df[df["Application Fees"] == "Y"]
        elif app_fee_filter == "No":
            df = df[df["Application Fees"] == "N"]
        elif app_fee_filter == "Blank":
            df = df[df["Application Fees"].isna() | (df["Application Fees"] == "")]

        # Degree Level Filter
        if "Degree Level" in df.columns:
            degrees = ["All"] + sorted(df["Degree Level"].dropna().unique().tolist())
            degree_filter = st.sidebar.selectbox("🎓 Degree Level", degrees)
            if degree_filter != "All":
                df = df[df["Degree Level"] == degree_filter]

        st.subheader("🎯 Filtered Results")
        st.write(f"Total programs found: {len(df)}")
        st.dataframe(df.reset_index(drop=True))

    except Exception as e:
        st.error("❌ Error reading the Excel file.")
        st.exception(e)
else:
    st.error("📁 'universities_courses.xlsx' not found in the repository. Please upload it to GitHub.")
