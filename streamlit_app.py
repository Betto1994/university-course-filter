import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="University Course Explorer", layout="wide")
st.title("🎓 University Course Explorer in Germany")

file_path = "universities_courses.xlsx"

# Check if file exists
if os.path.exists(file_path):
    try:
        # Load Excel file from specific sheet
        df = pd.read_excel(file_path, sheet_name="Data base")

        st.success("Excel file loaded successfully.")

        # Show data preview
        with st.expander("🔍 Preview Dataset"):
            st.dataframe(df)

        # Sidebar filters
        st.sidebar.header("📊 Filter Options")

        # Tuition Fees Filter
        fee_filter = st.sidebar.selectbox("💰 Tuition Fees", options=["All", "Free", "Paid"])
        if fee_filter == "Free":
            df = df[df["Tuition Fees"].str.upper() == "N"]
        elif fee_filter == "Paid":
            df = df[df["Tuition Fees"].str.upper() == "Y"]

        # Application Fees Filter
        app_fee_filter = st.sidebar.selectbox("💸 Application Fees", options=["All", "Yes", "No", "Blank"])
        if app_fee_filter == "Yes":
            df = df[df["Application Fees"].str.upper() == "Y"]
        elif app_fee_filter == "No":
            df = df[df["Application Fees"].str.upper() == "N"]
        elif app_fee_filter == "Blank":
            df = df[df["Application Fees"].isna() | (df["Application Fees"] == "")]

        # Intake Semester Filter
        if "Intake Semester" in df.columns:
            intake_options = ["All", "Winter", "Summer", "Winter and summer"]
            intake_filter = st.sidebar.selectbox("📅 Intake Semester", intake_options)
            if intake_filter != "All":
                df = df[df["Intake Semester"].str.lower() == intake_filter.lower()]

        # Degree Level Filter
        if "Degree Level" in df.columns:
            degrees = ["All"] + sorted(df["Degree Level"].dropna().unique().tolist())
            degree_filter = st.sidebar.selectbox("🎓 Degree Level", degrees)
            if degree_filter != "All":
                df = df[df["Degree Level"] == degree_filter]

        # Display results
        st.subheader("🎯 Filtered Results")
        st.write(f"Total programs found: {len(df)}")

        for idx, row in df.reset_index(drop=True).iterrows():
            with st.expander(f"📘 {row['Course Name']} — {row['University']}"):
                st.markdown(f"**Degree Level:** {row.get('Degree Level', 'N/A')}")
                st.markdown(f"**Intake Semester:** {row.get('Intake Semester', 'N/A')}")
                st.markdown(f"**Tuition Fees:** {'No' if row.get('Tuition Fees', '') == 'N' else 'Yes'}")
                st.markdown(f"**Application Fees:** {row.get('Application Fees', 'N/A')}")
                st.markdown("**Requirements:**")
                st.write(row.get("Requirements", "Not specified"))

    except Exception as e:
        st.error("❌ Error reading the Excel file.")
        st.exception(e)
else:
    st.error("📁 'universities_courses.xlsx' not found in the repository. Please upload it to GitHub.")
