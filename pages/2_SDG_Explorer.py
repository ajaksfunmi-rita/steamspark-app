import streamlit as st
import pandas as pd

# --- 1. SESSION STATE SAFETY CHECK ---
# Ensures 'db' and 'sdg' key exist even if the page is refreshed
if "db" not in st.session_state:
    st.session_state.db = {}

if "sdg" not in st.session_state.db:
    try:
        # Load the specific CSV for the SDG module
        st.session_state.db["sdg"] = pd.read_csv("STEAMspark_SDG_Explorer_Reference.csv")
    except Exception as e:
        st.error(f"Error: Could not find the SDG CSV file. {e}")
        st.stop()

# Ensure profile is ready
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Innovator", 
        "language": "English", 
        "score": 0
    }

# --- 2. PAGE SETUP & DATA HANDLING ---
st.header("🌍 SDG Explorer")
st.write(f"Changemaker {st.session_state.profile['name']}, let's discover how STEAM saves our planet!")

# Styling for the SDG Cards
st.markdown("""
    <style>
    .sdg-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #1B5E20;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .sdg-header { color: #1B5E20; font-weight: bold; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

sdg_df = st.session_state.db["sdg"]

# Navigation through the 17 Goals
if "sdg_index" not in st.session_state:
    st.session_state.sdg_index = 0

current_sdg = sdg_df.iloc[st.session_state.sdg_index]

# --- 3. DYNAMIC CONTENT MAPPING ---
# Logic to handle language suffixes (EN, YO, HA, IG)
lang_map = {"English": "EN", "Yoruba": "YO", "Hausa": "HA", "Igbo": "IG"}
lang_suffix = lang_map.get(st.session_state.profile['language'], "EN")

# Access columns dynamically to avoid further KeyErrors
goal_title = current_sdg['Goal'] 
overview = current_sdg[f'Overview_{lang_suffix}']
# Ensure the challenge column is pulled correctly
challenge_col = f'Challenge_{lang_suffix}'
challenge = current_sdg[challenge_col] if challenge_col in current_sdg else "Ready for a STEAM challenge?"

# --- 4. DISPLAY THE SDG CARD ---
st.markdown('<div class="sdg-card">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    # Basic logic for dynamic icons
    icon_symbol = "🌱" if "Life" in goal_title or "Green" in goal_title else "💧" if "Water" in goal_title else "☀️"
    st.title(icon_symbol)
    st.write(f"**Goal {current_sdg.get('Goal_Number', st.session_state.sdg_index + 1)}**")

with col2:
    st.markdown(f'<p class="sdg-header">{goal_title}</p>', unsafe_allow_html=True)
    st.write(f"**What it's about:** {overview}")

st.divider()
st.subheader("🚀 The STEAM Challenge")
st.info(challenge)
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. NAVIGATION & PROGRESS ---
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    if st.button("⬅️ Previous Goal") and st.session_state.sdg_index > 0:
        st.session_state.sdg_index -= 1
        st.rerun()

with c2:
    if st.button("Collect Badge 🏅"):
        st.balloons()
        st.toast(f"You earned the {goal_title} Badge!")
        st.session_state.profile['score'] += 50

with c3:
    if st.button("Next Goal ➡️") and st.session_state.sdg_index < len(sdg_df) - 1:
        st.session_state.sdg_index += 1
        st.rerun()

if st.button("Go to Tutorial Zone 🎥"):
    st.switch_page("pages/5_Tutorials.py")