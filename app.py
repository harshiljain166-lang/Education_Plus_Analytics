import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import LabelEncoder

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EduPulse Analytics ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0b1120;
        color: white;
    }

    .main {
        background: linear-gradient(135deg, #0b1120 0%, #111827 40%, #1e293b 100%);
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }

    .metric-card {
        background: linear-gradient(145deg, #111827, #1f2937);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        transition: 0.3s ease-in-out;
    }

    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0px 14px 30px rgba(0,0,0,0.5);
    }

    .metric-value {
        font-size: 34px;
        font-weight: 700;
        color: #38bdf8;
    }

    .metric-label {
        font-size: 15px;
        color: #d1d5db;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .stSelectbox label, .stSlider label {
        color: white !important;
        font-weight: 500;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
@st.cache_data

def load_data():
    df = pd.read_csv("xAPI-Edu-Data.csv")
    return df


df = load_data()

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class='glass-card'>
        <h1 style='text-align:center; color:#38bdf8;'>🎓 EduPulse Analytics Dashboard</h1>
        <p style='text-align:center; color:#cbd5e1; font-size:18px;'>
        Advanced Student Performance Intelligence System | Interactive Data Visualization | AI Driven Insights
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Dashboard Controls")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

selected_stage = st.sidebar.multiselect(
    "Select Educational Stage",
    options=df['StageID'].unique(),
    default=df['StageID'].unique()
)

selected_topic = st.sidebar.multiselect(
    "Select Topic",
    options=df['Topic'].unique(),
    default=df['Topic'].unique()
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df['gender'].isin(selected_gender)) &
    (df['StageID'].isin(selected_stage)) &
    (df['Topic'].isin(selected_topic))
]

# ---------------- KPI SECTION ----------------
student_count = filtered_df.shape[0]
avg_raised_hands = round(filtered_df['raisedhands'].mean(), 2)
avg_visits = round(filtered_df['VisITedResources'].mean(), 2)
avg_announcements = round(filtered_df['AnnouncementsView'].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{student_count}</div>
        <div class='metric-label'>Total Students</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{avg_raised_hands}</div>
        <div class='metric-label'>Avg Raised Hands</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{avg_visits}</div>
        <div class='metric-label'>Avg Resource Visits</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{avg_announcements}</div>
        <div class='metric-label'>Avg Announcement Views</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- CHART SECTION ----------------
col5, col6 = st.columns(2)

with col5:
    gender_chart = px.pie(
        filtered_df,
        names='gender',
        title='Gender Distribution',
        hole=0.55,
        template='plotly_dark'
    )

    gender_chart.update_traces(textinfo='percent+label')
    gender_chart.update_layout(
        title_font_size=22,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(gender_chart, use_container_width=True)

with col6:
    stage_chart = px.bar(
        filtered_df,
        x='StageID',
        color='StageID',
        title='Students by Educational Stage',
        template='plotly_dark',
        text_auto=True
    )

    stage_chart.update_layout(
        title_font_size=22,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    st.plotly_chart(stage_chart, use_container_width=True)

# ---------------- 3D VISUALIZATION ----------------
st.markdown("## 🚀 3D Student Performance Visualization")

fig_3d = px.scatter_3d(
    filtered_df,
    x='raisedhands',
    y='VisITedResources',
    z='AnnouncementsView',
    color='Class',
    size='Discussion',
    hover_name='Topic',
    template='plotly_dark',
    opacity=0.85,
    title='3D Student Engagement Mapping'
)

fig_3d.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        bgcolor='rgba(0,0,0,0)',
        xaxis_title='Raised Hands',
        yaxis_title='Visited Resources',
        zaxis_title='Announcement Views'
    )
)

st.plotly_chart(fig_3d, use_container_width=True)

# ---------------- HEATMAP ----------------
st.markdown("## 📊 Correlation Intelligence Matrix")

numeric_cols = [
    'raisedhands',
    'VisITedResources',
    'AnnouncementsView',
    'Discussion'
]

corr = filtered_df[numeric_cols].corr()

heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=corr.values.round(2),
        texttemplate="%{text}",
        colorscale='Blues'
    )
)

heatmap.update_layout(
    template='plotly_dark',
    title='Feature Correlation Heatmap',
    title_font_size=22,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(heatmap, use_container_width=True)

# ---------------- PERFORMANCE ANALYSIS ----------------
col7, col8 = st.columns(2)

with col7:
    performance_chart = px.histogram(
        filtered_df,
        x='Class',
        color='Class',
        template='plotly_dark',
        title='Performance Class Distribution',
        text_auto=True
    )

    performance_chart.update_layout(
        title_font_size=22,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(performance_chart, use_container_width=True)

with col8:
    topic_chart = px.treemap(
        filtered_df,
        path=['Topic'],
        values='raisedhands',
        color='raisedhands',
        template='plotly_dark',
        title='Topic Engagement Treemap'
    )

    topic_chart.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=22
    )

    st.plotly_chart(topic_chart, use_container_width=True)

# ---------------- ADVANCED ANALYTICS ----------------
st.markdown("## 📈 Student Behaviour Insights")

behavior_chart = px.scatter(
    filtered_df,
    x='VisITedResources',
    y='raisedhands',
    color='Class',
    size='Discussion',
    hover_data=['Topic', 'StageID'],
    template='plotly_dark',
    title='Learning Activity vs Participation'
)

behavior_chart.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_font_size=22
)

st.plotly_chart(behavior_chart, use_container_width=True)

# ---------------- RAW DATA ----------------
with st.expander("🔍 Explore Raw Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <div style='text-align:center; color:#94a3b8;'>
        Designed for Professional Portfolio & Technical Interviews 🚀<br>
        Built using Streamlit + Plotly + Advanced UI/UX Design
    </div>
    """,
    unsafe_allow_html=True
)
