import streamlit as st
import pandas as pd
import random

# --- 1. SESSION STATE SAFETY CHECK ---
# Ensures 'db' and 'ignite' key exist even if the page is refreshed
if "db" not in st.session_state:
    st.session_state.db = {}

if "ignite" not in st.session_state.db:
    try:
        # Load the specific CSV for the Science Quiz module
        st.session_state.db["ignite"] = pd.read_csv("STEAMspark_Ignite_Spark_50_Questions.csv")
    except Exception as e:
        st.error(f"Error: Could not find the Ignite Spark CSV file. {e}")
        st.stop()

# Ensure profile is initialized
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Innovator", 
        "language": "English", 
        "interest": "Science", 
        "score": 0
    }

# --- 2. DATA LOAD & FILTERING ---
df = st.session_state.db["ignite"]

# Filter questions based on the subject chosen in main.py
user_interest = st.session_state.profile["interest"]
# Safety check for Tech/Technology naming mismatch
if user_interest == "Tech":
    user_interest = "Technology"

subject_df = df[df['Subject'] == user_interest]

if subject_df.empty:
    st.warning(f"No questions found for {user_interest}. Showing all Science questions instead.")
    subject_df = df[df['Subject'] == 'Science']

# --- 3. GAMEPLAY STATE ---
if "ignite_index" not in st.session_state:
    st.session_state.ignite_index = random.randint(0, len(subject_df) - 1)

question_row = subject_df.iloc[st.session_state.ignite_index]

# --- 4. DYNAMIC COLUMN DETECTION (Solves ID & KeyError) ---
lang_map = {"English": "EN", "Yoruba": "YO", "Hausa": "HA", "Igbo": "IG"}
lang_suffix = lang_map.get(st.session_state.profile['language'], "EN")

all_cols = subject_df.columns.tolist()
# Find Question and Answer columns based on language suffix
q_col = next((c for c in all_cols if "Question" in c and lang_suffix in c), all_cols[1])
a_col = next((c for c in all_cols if "Answer" in c and lang_suffix in c), all_cols[2])

# --- 5. UI DISPLAY ---
st.header("⚡ Ignite Spark")
st.subheader(f"Subject: {user_interest}")

# Display the actual question text
st.info(f"❓ **Question:** {question_row[q_col]}")

# Multiple Choice Logic
correct_answer = str(question_row[a_col])
# Get distractors from the same column
distractors = subject_df[a_col].dropna().unique().tolist()
if correct_answer in distractors:
    distractors.remove(correct_answer)

options = random.sample(distractors, min(len(distractors), 3)) + [correct_answer]
random.shuffle(options)

user_choice = st.radio("Choose your answer:", options)

if st.button("Submit Answer"):
    if user_choice == correct_answer:
        st.success("🌟 Correct! You've earned 25 points!")
        st.session_state.profile['score'] += 25
    else:
        st.error(f"Not quite. The correct answer was: {correct_answer}")

# --- 6. NAVIGATION ---
st.divider()
if st.button("Next Question ➡️"):
    st.session_state.ignite_index = random.randint(0, len(subject_df) - 1)
    st.rerun()

if st.button("Back to Hub 🏠"):
    st.switch_page("main.py")