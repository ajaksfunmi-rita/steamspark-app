import streamlit as st
import pandas as pd
import random

# --- 1. SESSION STATE SAFETY CHECK ---
# Ensures 'db' exists and has the 'idiom' key
if "db" not in st.session_state:
    st.session_state.db = {}

if "idiom" not in st.session_state.db:
    try:
        # Load the specific CSV for this module
        st.session_state.db["idiom"] = pd.read_csv("STEAMspark_IdiomQuest_50_Questions.csv")
    except Exception as e:
        st.error(f"Error: Could not find the Idiom CSV file. {e}")
        st.stop()

# Ensure profile is ready
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "Innovator", "language": "English", "interest": "Science", "score": 0}

# --- 2. DATA LOAD & LANGUAGE SETUP ---
idiom_df = st.session_state.db["idiom"]
lang_map = {"English": "EN", "Yoruba": "YO", "Hausa": "HA", "Igbo": "IG"}
lang_suffix = lang_map.get(st.session_state.profile['language'], "EN")

# --- 3. DYNAMIC COLUMN DETECTION (Solves ID issue) ---
all_cols = idiom_df.columns.tolist()
# Find columns for Idiom and Meaning based on language
idiom_col = next((c for c in all_cols if "Idiom" in c and lang_suffix in c), None)
meaning_col = next((c for c in all_cols if "Meaning" in c and lang_suffix in c), None)

# Fallback to avoid the ID column at index 0
if not idiom_col:
    idiom_col = all_cols[1]
if not meaning_col:
    meaning_col = all_cols[2]

# --- 4. GAMEPLAY STATE ---
if "idiom_index" not in st.session_state:
    st.session_state.idiom_index = random.randint(0, len(idiom_df) - 1)

current_row = idiom_df.iloc[st.session_state.idiom_index]

# --- 5. UI DISPLAY ---
st.header("🗣️ Idiom Quest")
st.subheader("What does this idiom mean?")

# Display actual text content
st.info(f"📜 Idiom: **{current_row[idiom_col]}**")

# Prepare Quiz Options
correct_answer = current_row[meaning_col]
distractors = idiom_df[meaning_col].dropna().unique().tolist()
if correct_answer in distractors:
    distractors.remove(correct_answer)

options = random.sample(distractors, min(len(distractors), 3)) + [correct_answer]
random.shuffle(options)

user_choice = st.radio("Choose the correct meaning:", options)

if st.button("Check Answer"):
    if user_choice == correct_answer:
        st.success("🎉 Correct!")
        st.session_state.profile['score'] += 20
    else:
        st.error(f"Not quite. The correct meaning is: {correct_answer}")

# --- 6. NAVIGATION ---
st.divider()
if st.button("Try Another Idiom 🔄"):
    st.session_state.idiom_index = random.randint(0, len(idiom_df) - 1)
    st.rerun()

if st.button("Back to Hub 🏠"):
    st.switch_page("main.py")