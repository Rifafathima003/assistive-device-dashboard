

import streamlit as st
import pandas as pd
from clean import load_and_clean_data
# ---------------- LOAD DATA ----------------
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Assistive Device Dashboard", layout="wide", initial_sidebar_state="expanded")

st_autorefresh(interval=120000, key="autorefresh")

@st.cache_data(ttl=120)
def load_data_streamlit():
    return load_and_clean_data()        
df=load_data_streamlit()

# ---------------- TITLE ----------------
st.title("📊 Assistive Device Needs Dashboard")

st.markdown("Comprehensive view of device requirements across schools and districts")
st.markdown("---")
st.divider()

# ---------------- GLOBAL METRICS ----------------
st.markdown(""" <style>.kpi-card {background-color: #1E1E2E; border-radius: 12px; padding: 20px; text-align: center; color: white;}</style> """, unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
 
with col1:
    st.markdown(f"<div class='kpi-card'><h3>Total Devices</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><h3>Total Schools</h3><h1>{df['School_Name'].nunique()}</h1></div>", unsafe_allow_html=True)    
with col3:
    st.markdown(f"<div class='kpi-card'><h3>Total Districts</h3><h1>{df['District'].nunique()}</h1></div>", unsafe_allow_html=True)

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
st.markdown("##📦 Total Device Requirement")

col1, col2 = st.columns(2)

col1.metric("Devices per District", round(len(filtered_df)/ filtered_df['District'].nunique(), 1))
col2.metric("Devices per School", round(len(filtered_df)/ filtered_df['School_Name'].nunique(), 1))
col3.metric("Most Needed Device", filtered_df['Device'].value_counts().idxmax())

import plotly.express as px
# ==================== DISTRIBUTION ANALYSIS ====================
st.markdown("## 📊 Distribution Analysis")
st.markdown("<br>", unsafe_allow_html=True)

# -------------------- ROW 1 --------------------
col1, col2 = st.columns(2)

# 🔧 DEVICE DISTRIBUTION (GREEN)
with col1:
    st.markdown("### 🔧 Device Distribution")

    device_counts = (
        filtered_df['Device']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Device', 'Device': 'Count'})
        .sort_values(by='Count', ascending=False)
    )

    fig = px.bar(
        device_counts,
        x='Device',
        y='Count',
        color='Count',
        color_continuous_scale='Greens'
    )

    fig.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

# 🧩 DEVICE CATEGORY (PURPLE)
with col2:
    st.markdown("### 🧩 Device Category Distribution")

    category_counts = (
        filtered_df['Device Category']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Category', 'Device Category': 'Count'})
        .sort_values(by='Count', ascending=False)
    )

    fig = px.bar(
        category_counts,
        x='Category',
        y='Count',
        color='Count',
        color_continuous_scale='Purples'
    )

    fig.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------- ROW 2 --------------------
col3, col4 = st.columns(2)

# ⚡ PRIORITY (ORANGE)
with col3:
    st.markdown("### ⚡ Device Priority Distribution")

    priority_counts = (
        filtered_df['Priority']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Priority', 'Priority': 'Count'})
        .sort_values(by='Count', ascending=False)
    )

    fig = px.bar(
        priority_counts,
        x='Priority',
        y='Count',
        color='Count',
        color_continuous_scale='Oranges'
    )

    fig.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

# ♿ DISABILITY (BLUE)
with col4:
    st.markdown("### ♿ Disability Distribution")

    disability_counts = (
        filtered_df['disability_cleaned']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Disability', 'disability_cleaned': 'Count'})
        .sort_values(by='Count', ascending=False)
    )

    fig = px.bar(
        disability_counts,
        x='Disability',
        y='Count',
        color='Count',
        color_continuous_scale='Blues'
    )

    fig.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------- ROW 3 --------------------
col5, col6 = st.columns(2)

# 👥 SOCIAL CATEGORY (MAGMA STYLE)
with col5:
    st.markdown("### 👥 Social Category Distribution")

    social_counts = (
        filtered_df['Social Category']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Category', 'Social Category': 'Count'})
        .sort_values(by='Count', ascending=False)
    )

    fig = px.bar(
        social_counts,
        x='Category',
        y='Count',
        color='Count',
        color_continuous_scale='Magma'
    )

    fig.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

# 🚻 GENDER (CUSTOM COLORS)
with col6:
    st.markdown("### 🚻 Gender Distribution")

    gender_counts = (
        filtered_df['Gender']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Gender', 'Gender': 'Count'})
        .sort_values(by='Count', ascending=False)
    )

    fig = px.pie(
        gender_counts,
        names='Gender',
        values='Count',
        color_discrete_sequence=['#4CAF50', '#2196F3']
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------- OPTIONAL DATA VIEW ----------------
with st.expander("📄 View  & Download Filtered Data"):
    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_device_data.csv',
        mime='text/csv'
    )