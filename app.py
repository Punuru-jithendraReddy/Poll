import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION ---
# 1. Your Google Form POST URL (Change /viewform to /formResponse)
GOOGLE_FORM_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?output=csv"

# 2. Your Google Form Entry IDs (You must find these by getting a "Pre-filled link" from your form)
ENTRY_EMAIL = "entry.111111" 
ENTRY_NAME = "entry.222222"
ENTRY_MAGIC = "entry.333333" # The column where the multi-select votes go

# 3. Your Published Google Sheet CSV Link (for the dashboard)
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/YOUR_SHEET_ID/pub?output=csv"

# --- MOCK DATA FOR 300 NAMES ---
# Replace this list with your actual 300 Excel names
ALL_NAMES = [f"Participant {i}" for i in range(1, 301)]

# --- PAGE SETUP & IOS UI ---
st.set_page_config(page_title="Premium Poll", page_icon="📊", layout="wide")

st.markdown("""
<style>
    /* iOS & Apple Premium Aesthetic */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #f5f5f7; /* Apple light gray */
        color: #1d1d1f;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Floating Card Style for inputs */
    .stTextInput > div > div > input, .stTextArea > div > textarea {
        border-radius: 12px;
        border: 1px solid #d2d2d7;
        padding: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    /* Primary iOS Button */
    div.stButton > button {
        background: linear-gradient(180deg, #007aff 0%, #0056b3 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 122, 255, 0.4);
        color: white;
    }

    /* Dashboard Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1d1d1f;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT FOR BULK PASTE ---
if 'selected_names' not in st.session_state:
    st.session_state.selected_names = []

# --- APP LAYOUT ---
st.title("Cast Your Vote")
st.markdown("Select your designated items. You can search manually or bulk-paste from Excel.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Identity Verification")
    user_email = st.text_input("Email address")
    user_name = st.selectbox("Please select your name", ["Your Name Here", "Admin", "User"])

with col2:
    st.markdown("### 2. Bulk Excel Import")
    st.caption("Paste a column of names directly from Excel to auto-select them below.")
    bulk_paste = st.text_area("Paste from clipboard:", height=100)
    
    if st.button("Auto-Check Pasted Names"):
        if bulk_paste:
            # Clean and match pasted lines to the master list
            pasted_lines = [line.strip() for line in bulk_paste.split('\n') if line.strip() in ALL_NAMES]
            
            # Combine current selections with pasted ones, avoiding duplicates
            combined = list(set(st.session_state.selected_names + pasted_lines))
            st.session_state.selected_names = combined
            st.rerun()

st.divider()

# --- THE SEARCHABLE MULTI-SELECT ---
st.markdown("### 3. Selection Roster")
selected = st.multiselect(
    "Search and select (or review bulk-pasted targets):",
    options=ALL_NAMES,
    default=st.session_state.selected_names,
    key="live_selection"
)

# Update session state based on manual changes
st.session_state.selected_names = selected

# --- SUBMISSION LOGIC ---
if st.button("Submit to Database"):
    if not user_email or not selected:
        st.error("Please provide your email and select at least one target.")
    else:
        with st.spinner("Encrypting and transmitting..."):
            # Join multiple selections with a comma (standard Google Form behavior)
            magic_data = ", ".join(selected)
            
            payload = {
                ENTRY_EMAIL: user_email,
                ENTRY_NAME: user_name,
                ENTRY_MAGIC: magic_data
            }
            
            try:
                response = requests.post(GOOGLE_FORM_URL, data=payload)
                if response.status_code == 200:
                    st.success("Your response has been recorded in the Google Sheet.")
                    st.balloons()
                    st.session_state.selected_names = [] # Clear the form
                else:
                    st.error("Submission failed. Check your Form URL and Entry IDs.")
            except Exception as e:
                st.error(f"Network error: {e}")

st.divider()

# --- PREMIUM DASHBOARD: TOP 30 ---
st.markdown("## Live Leaderboard")
st.caption("Top 30 designations based on live Google Sheet data.")

try:
    # Read live data directly from the published CSV link
    df = pd.read_csv(GOOGLE_SHEET_CSV)
    
    # Assuming your Google Form column header is exactly "Please select the youre magic..."
    magic_column_name = [col for col in df.columns if "magic" in col.lower()][0]
    
    # Google Forms puts multi-select answers in one cell separated by commas. We must explode them.
    all_votes = df[magic_column_name].dropna().astype(str)
    split_votes = all_votes.str.split(',').explode().str.strip()
    
    # Count occurrences and grab top 30
    top_30 = split_votes.value_counts().head(30)
    
    if not top_30.empty:
        # Create a beautiful iOS-style bar chart
        st.bar_chart(top_30, color="#007aff", height=400)
    else:
        st.info("Awaiting initial telemetry. No votes logged yet.")
        
except Exception as e:
    st.warning("Dashboard offline. Ensure you have 'Published to Web' your Google Sheet as a CSV and pasted the correct link.")
