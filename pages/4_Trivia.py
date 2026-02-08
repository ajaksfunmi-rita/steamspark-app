import streamlit as st
import pandas as pd
import random

# --- 1. SESSION STATE SAFETY CHECK ---
# We verify the database AND the specific 'trivia' key exist
if "db" not in st.session_state:
    st.session_state.db = {}

if "trivia" not in st.session_state.db:
    try:
        # Manually loading to ensure the 'trivia' key is populated
        st.session_state.db["trivia"] = pd.read_csv("STEAMspark_RandomTrivia_50_Unique_Questions.csv")
    except Exception as e:
        st.error(f"Error: Could not find the Trivia CSV file. {e}")
        st.stop()

# Ensure profile is ready
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "Innovator", "language": "English", "interest": "Science", "score": 0}

# --- 2. DATA LOAD ---
trivia_df = st.session_state.db["trivia"]

# --- 3. SESSION STATE FOR GAMEPLAY ---
if "trivia_index" not in st.session_state:
    st.session_state.trivia_index = random.randint(0, len(trivia_df) - 1)
    st.session_state.reveal = False

# Select the specific row
card = trivia_df.iloc[st.session_state.trivia_index]

# --- 4. COLUMN SELECTION BY POSITION ---
# .iloc[1] = 2nd Column (Question)
# .iloc[6] = 7th Column (Answer)
# This prevents IDs from showing and avoids KeyErrors
question_text = card.iloc[2] 
answer_text = card.iloc[6] 

# --- 5. UI DISPLAY ---
st.header("💡 STEAM Trivia")

st.subheader("The Question:")
st.info(f"❓ {question_text}")

st.divider()

# Reveal Logic
if not st.session_state.reveal:
    if st.button("🔓 Reveal Answer"):
        st.session_state.reveal = True
        st.rerun()
else:
    st.markdown("### ✅ The Answer:")
    st.success(answer_text)
    
    if st.button("I got it right! +10 Points"):
        st.session_state.profile['score'] += 10
        st.balloons()
        st.toast("Points Added!")

# --- 6. NAVIGATION ---
if st.button("Next Trivia Question 🔄"):
    st.session_state.trivia_index = random.randint(0, len(trivia_df) - 1)
    st.session_state.reveal = False
    st.rerun()

if st.button("Back to Hub 🏠"):
    st.switch_page("main.py")