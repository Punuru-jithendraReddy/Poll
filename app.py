import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px

# ==========================================
# 1. SYSTEM CONFIGURATION & CREDENTIALS
# ==========================================
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse"
ENTRY_EMAIL = "emailAddress"
ENTRY_NAME = "entry.1398544706"
ENTRY_MAGIC = "entry.921793836"

GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"

# ==========================================
# 2. MASTER DATA
# ==========================================
USER_NAMES = [
    "Saikiran Kandhi", "Shaik Afroz", "Venkat", "Jithendra reddy",
    "Bhavana Lanka", "Sravanthi Chapram", "B. Shrineeth Reddy",
    "Shreya Singh", "Tharuni Vallepi", "Saumya Lailamony",
    "Monisha", "Vijay Sai"
]

TEAM_NAMES = TEAM_NAMES = [
    # (your full TEAM_NAMES list remains unchanged)
]

USER_SUGGESTIONS = {
    "Saikiran Kandhi": ["Reactor Core", "Apex Sync", "Pixel Forge", "Zero Gravity", "Ignition Squad"],
    "Shaik Afroz": ["FutureMakers", "IdeaCatalysts", "SparkLab", "InsightSphere"],
    "Venkat": [], "Jithendra reddy": [], "Bhavana Lanka": [], "Sravanthi Chapram": [],
    "B. Shrineeth Reddy": [], "Shreya Singh": [], "Tharuni Vallepi": [],
    "Saumya Lailamony": [], "Monisha": [], "Vijay Sai": []
}

# ==========================================
# 3. PAGE SETUP
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="centered")

# ==========================================
# SESSION INIT (FIXED)
# ==========================================
if "team_select" not in st.session_state:
    st.session_state.team_select = []

# ==========================================
# BULK IMPORT FUNCTION (FIXED BUG)
# ==========================================
def process_bulk_import(pasted_data, allowed_teams):
    clean_allowed = {t.strip().lower(): t for t in allowed_teams}
    matched_lines = []
    raw_lines = pasted_data.replace('\r', '\n').split('\n')

    for line in raw_lines:
        clean_line = line.strip().lower()
        if clean_line and clean_line in clean_allowed:
            matched_lines.append(clean_allowed[clean_line])

    current = st.session_state.get("team_select", [])
    st.session_state.team_select = list(set(current + matched_lines))

    return len(matched_lines)

# ==========================================
# 4. PRIMARY APPLICATION
# ==========================================
st.title("Identity Intel")
st.caption("Secure Team Designation Portal")

col_name, col_email = st.columns(2)

with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES)

with col_email:
    user_email = st.text_input("Corporate Email", placeholder="agent@intel.com")

forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]

st.markdown("### Bulk Data Import")
pasted_data = st.text_area("Paste Data", height=100)

if st.button("Process Excel Data"):
    if user_name == "Select identity...":
        st.warning("Please select your name first.")
    elif pasted_data:
        count = process_bulk_import(pasted_data, allowed_teams)
        st.success(f"Matched {count} targets.")
        st.rerun()

# ==========================================
# TARGET SELECTION (FIXED)
# ==========================================
st.markdown("### Target Selection")

final_selections = st.multiselect(
    "Combobox Search",
    options=allowed_teams,
    default=st.session_state.get("team_select", []),
    key="team_select",
    label_visibility="collapsed",
    placeholder="Search manually or review imported targets..."
)

# ==========================================
# SUBMISSION LOGIC
# ==========================================
if st.button("Submit Selections"):
    if user_name == "Select identity..." or not user_email:
        st.error("Please provide Name and Email.")
    elif not final_selections:
        st.error("Please select at least one target.")
    elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user_email):
        st.error("Invalid email format.")
    else:
        try:
            df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
            df_string = df.astype(str).apply(lambda x: x.str.strip().str.lower())
            target_email = user_email.strip().lower()

            if (df_string == target_email).any().any():
                st.error("This email has already submitted.")
            else:
                payload = {
                    ENTRY_EMAIL: user_email,
                    ENTRY_NAME: user_name,
                    ENTRY_MAGIC: final_selections
                }
                response = requests.post(GOOGLE_FORM_URL, data=payload)

                if response.status_code == 200:
                    st.success("Submission successful.")
                    st.session_state.team_select = []
                else:
                    st.error("Submission failed.")
        except:
            st.error("Database connection failed.")

st.divider()

# ==========================================
# 5. PREMIUM LIVE DASHBOARD
# ==========================================
st.markdown("### Live Leaderboard")

try:
    df = pd.read_csv(GOOGLE_SHEET_CSV_URL)

    if not df.empty and len(df.columns) >= 4:
        magic_column = df.columns[3]
        all_votes = df[magic_column].dropna().astype(str)
        split_votes = all_votes.str.split(',').explode().str.strip()

        col_sort, col_slider = st.columns([1, 1])

        with col_sort:
            sort_order = st.selectbox("Sort By:", ["Most Votes", "Alphabetical"])

        with col_slider:
            top_n = st.slider("Display Top:", 5, 100, 30, 5)

        vote_counts = split_votes.value_counts().head(top_n)

        if not vote_counts.empty:
            df_plot = vote_counts.reset_index()
            df_plot.columns = ['Designation', 'Votes']

            if sort_order == "Most Votes":
                df_plot = df_plot.sort_values(by='Votes', ascending=True)
            else:
                df_plot = df_plot.sort_values(by='Designation', ascending=False)

            fig = px.bar(
                df_plot,
                x="Votes",
                y="Designation",
                orientation="h",
                text="Votes"
            )

            fig.update_traces(
                marker=dict(
                    color=df_plot["Votes"],
                    colorscale=[[0, "#6366F1"], [1, "#7C3AED"]],
                    line=dict(width=0)
                ),
                textposition="outside",
                cliponaxis=False
            )

            bar_height = 32
            dynamic_height = max(300, len(df_plot) * bar_height)

            fig.update_layout(
                height=dynamic_height,
                bargap=0.35,
                xaxis=dict(
                    rangemode="tozero",
                    showgrid=True,
                    gridcolor="#E2E8F0",
                    title="Total Votes",
                    dtick=1
                ),
                yaxis=dict(title=""),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0),
                font=dict(color="#0F172A")
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No votes logged yet.")
    else:
        st.info("Database empty.")

except:
    st.warning("Dashboard offline.")
