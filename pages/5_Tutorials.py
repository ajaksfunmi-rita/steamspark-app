import streamlit as st
import pandas as pd

# --- SAFETY INITIALIZATION ---
# This fixes the "db not found" error if you refresh the page
if "db" not in st.session_state:
    st.session_state.db = {
        "tutorial": pd.read_csv("STEAMspark_TutorialZone_Manifest.csv")
    }

if "profile" not in st.session_state:
    st.session_state.profile = {"name": "Innovator", "language": "English", "interest": "Science", "score": 0}

# --- DATA LOAD ---
tutorial_df = st.session_state.db["tutorial"]
lang_map = {"English": "EN", "Yoruba": "YO", "Hausa": "HA", "Igbo": "IG"}
lang_suffix = lang_map.get(st.session_state.profile['language'], "EN")

# Detect Columns
all_cols = tutorial_df.columns.tolist()
title_col = next((c for c in all_cols if "Title" in c and lang_suffix in c), "Title_EN")
link_col = next((c for c in all_cols if "Link" in c and lang_suffix in c), "Link_EN")

st.header("🎥 Tutorial Zone")

# Clean the interest name to match CSV
user_interest = st.session_state.profile["interest"]
if user_interest == "Tech": 
    user_interest = "Technology"

# Filter the data
subject_tutorials = tutorial_df[tutorial_df['Subject'] == user_interest]

if not subject_tutorials.empty:
    selected_title = st.selectbox("Choose a Lesson:", subject_tutorials[title_col].tolist())
    lesson_row = subject_tutorials[subject_tutorials[title_col] == selected_title].iloc[0]
    
    # Reveal the video
    video_url = str(lesson_row[link_col]).strip()
    if "http" in video_url:
        st.video(video_url)
    else:
        st.warning(f"Video link missing for {selected_title}")
else:
    st.error(f"No tutorials found for '{user_interest}'. Check your CSV 'Subject' column!")

if st.button("Back to Hub 🏠"):
    st.switch_page("main.py")