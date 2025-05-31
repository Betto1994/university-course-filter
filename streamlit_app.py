import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="University Course Explorer", layout="wide")
st.title("🎓 University Course Explorer in Germany")

file_path = "universities_courses.xlsx"

# Check if file exists
if os.path.exists(file_path):
    try:
        # Load Excel file
        df = pd.read_excel(file_path)

        st.success("Excel file loaded successfully.")

        # Show data preview
        with st.expander("🔍 Preview Dataset"):
            st.dataframe(df)

        # Filters
        st.sidebar.header("📊 Filter Options")

        # Tuition fee filter
        fee_filter = st.sidebar.selectbox("💰 Tuition Fees", options=["All", "Free", "Paid"])
        if fee_filter == "Free":
            df = df[df["Tuition Fee"].str.lower().str.contains("free")]
        elif fee_filter == "Paid":
            df = df[df["Tuition Fee"].str.lower().str.contains("€")]

        # Degree level filter
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

