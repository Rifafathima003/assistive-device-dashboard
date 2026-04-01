

import streamlit as st
import pandas as pd
from clean import load_and_clean_data
# ---------------- LOAD DATA ----------------
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=120000, key="autorefresh")

@st.cache_data(ttl=120)
def load_data_streamlit():
    return load_and_clean_data()        
df=load_data_streamlit()

st.set_page_config(page_title="Assistive Device Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.title("📊 Assistive Device Needs Dashboard")

st.markdown("Comprehensive view of device requirements across schools and districts")

st.divider()

# ---------------- GLOBAL METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Devices Required", len(df))
col2.metric("Total Schools", df['School_Name'].nunique())
col3.metric("Total Districts", df['District'].nunique())

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar. header ("🔁 Controls")

if st.sidebar.button ("Refresh Data"):
    st. cache_data.clear()
    st.rerun()
st.sidebar.markdown("---")

st.sidebar.header("🔍 Filters")

# -------- DISTRICT FILTER --------
districts = sorted(df['District'].dropna().unique())
# District Select All
select_all_districts = st.sidebar.checkbox("Select All Districts", value=True)

if select_all_districts:
    selected_districts = districts
else:
    selected_districts = st.sidebar.multiselect(
        "Select District",
        options=districts
    )


# -------- SCHOOL FILTER --------
schools = sorted(df['School_Name'].dropna().unique())
select_all_schools = st.sidebar.checkbox("Select All Schools", value=True)

if select_all_schools:
    selected_schools = schools
else:
    selected_schools = st.sidebar.multiselect(
        "Select School",
        options=schools
    )

# -------- DEVICE FILTER --------
devices = sorted(df['Device'].dropna().unique())
select_all_devices = st.sidebar.checkbox("Select All Devices", value=True)

if select_all_devices:
    selected_devices = devices
else:
    selected_devices = st.sidebar.multiselect(
        "Select Device",
        options=devices
    )

# -------- PRIORITY FILTER --------
if 'Priority' in df.columns:
    priorities = sorted(df['Priority'].dropna().unique())
    select_all_priorities = st.sidebar.checkbox("Select All Priorities", value=True)

    if select_all_priorities:
        selected_priorities = priorities
    else:
        selected_priorities = st.sidebar.multiselect(
            "Select Priority",
            options=priorities
        )
else:
    selected_priorities = None

# -------- GENDER FILTER --------
genders = sorted(df['Gender'].dropna().unique())
select_all_genders = st.sidebar.checkbox("Select All Genders", value=True)

if select_all_genders:
    selected_genders = genders
else:
    selected_genders = st.sidebar.multiselect(
        "Select Gender",
        options=genders
    )

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df['District'].isin(selected_districts)) &
    (df['School_Name'].isin(selected_schools)) &
    (df['Device'].isin(selected_devices)) &
    (df['Gender'].isin(selected_genders))
]

# Apply priority only if exists
if selected_priorities is not None:
    filtered_df = filtered_df[filtered_df['Priority'].isin(selected_priorities)]
# ---------------- TOTAL DEVICE COUNT ----------------
st.subheader("📦 Total Device Requirement")

col1, col2 = st.columns(2)

col1.metric("District Total Devices", len(filtered_df))
col2.metric("School Total Devices", len(filtered_df))

# ---------------- DEVICE COUNT ----------------
st.subheader("🔧 Device Distribution")

st.bar_chart(filtered_df['Device'].value_counts())

# ---------------- DEVICE CATEGORY ----------------
st.subheader("🧩 Device Category Distribution")

st.bar_chart(filtered_df['Device Category'].value_counts())

st.subheader("Device Priority Distribution ")
st.bar_chart(filtered_df['Priority'].value_counts())  

# ---------------- DISABILITY CATEGORY ----------------
st.subheader("♿ Disability Category Distribution")

st.bar_chart(filtered_df['disability_cleaned'].value_counts())

# ---------------- SOCIAL CATEGORY ----------------
st.subheader("👥 Social Category Distribution")

st.bar_chart(filtered_df['Social Category'].value_counts())

# ---------------- GENDER RATIO (SCHOOL) ----------------
st.subheader("👩‍🦰👨 Gender Distribution (School)")

gender_school = filtered_df['Gender'].value_counts()

st.bar_chart(gender_school)

# ---------------- GENDER RATIO (DISTRICT) ----------------
st.subheader("👩‍🦰👨 Gender Distribution (District)")

gender_district = filtered_df['Gender'].value_counts()

st.bar_chart(gender_district)

# ---------------- DISTRICT LEVEL DEVICE ANALYSIS ----------------
st.subheader("🏙 Device Distribution (District Level)")

st.bar_chart(filtered_df['Device'].value_counts())

# ---------------- DISTRICT CATEGORY ANALYSIS ----------------
st.subheader("🧩 Device Category (District Level)")

st.bar_chart(filtered_df['Device Category'].value_counts())

# ---------------- OPTIONAL DATA VIEW ----------------
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered_df)