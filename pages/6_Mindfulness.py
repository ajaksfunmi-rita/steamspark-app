import streamlit as st
import pandas as pd

# --- 1. SESSION STATE SAFETY CHECK ---
# Ensures 'db' and 'mindful' key exist even if the page is refreshed
if "db" not in st.session_state:
    st.session_state.db = {}

if "mindful" not in st.session_state.db:
    try:
        # Load the specific CSV for the Mindfulness module
        st.session_state.db["mindful"] = pd.read_csv("STEAMspark_Mindfulness_10_Day_Journey.csv")
    except Exception as e:
        st.error(f"Error: Could not find the Mindfulness CSV file. {e}")
        st.stop()

# Ensure profile is initialized
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Innovator", 
        "language": "English", 
        "score": 0
    }

# --- 2. DATA LOAD & LANGUAGE SETUP ---
mindful_df = st.session_state.db["mindful"]
lang_map = {"English": "EN", "Yoruba": "YO", "Hausa": "HA", "Igbo": "IG"}
lang_suffix = lang_map.get(st.session_state.profile['language'], "EN")

# --- 3. DYNAMIC COLUMN DETECTION (Solves ID & KeyError) ---
all_cols = mindful_df.columns.tolist()
# Find columns for the Activity and Reflection based on language
act_col = next((c for c in all_cols if "Activity" in c and lang_suffix in c), all_cols[1])
ref_col = next((c for c in all_cols if "Reflection" in c and lang_suffix in c), all_cols[2])

# --- 4. UI DISPLAY ---
st.header("🧘 Mindfulness Journey")
st.write(f"Welcome back, {st.session_state.profile['name']}. Take a deep breath.")

# Day Selection
day_options = mindful_df.index.tolist()
selected_day_idx = st.select_slider("Select your journey day:", options=day_options, value=0)

current_day = mindful_df.iloc[selected_day_idx]

st.markdown("---")
# Display actual content from the CSV
st.subheader(f"☀️ Day {selected_day_idx + 1}")
st.info(f"**Today's Activity:** {current_day[act_col]}")
st.success(f"**Reflect on this:** {current_day[ref_col]}")

# Progress Tracking
if st.button("I completed today's journey ✨"):
    st.session_state.profile['score'] += 10
    st.balloons()
    st.toast("Peace of mind earned! +10 Points")

# --- 5. NAVIGATION ---
st.divider()
if st.button("Back to Hub 🏠"):
    st.switch_page("main.py")