import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="centered")

# ==========================================
# 2. CONFIGURATION & STATE
# ==========================================
@st.cache_resource
def get_global_config():
    return {"end_time": None, "is_active": False}

global_config = get_global_config()

# Initialize Session State
if "submitted_emails" not in st.session_state: st.session_state.submitted_emails = set()
if "success_flag" not in st.session_state: st.session_state.success_flag = False
if "submission_error" not in st.session_state: st.session_state.submission_error = None
if "last_known_is_open" not in st.session_state: st.session_state.last_known_is_open = False

# --- KEY ROTATION (The Fix for Transmission Error) ---
# We increment this number to force-reset the widget safely
if "form_id" not in st.session_state: st.session_state.form_id = 0

# URLS
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse"
ENTRY_EMAIL = "emailAddress"
ENTRY_NAME = "entry.1398544706"
ENTRY_MAGIC = "entry.921793836"
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"

# ==========================================
# 3. MASTER DATA
# ==========================================
USER_NAMES = [
    "Select identity...", 
    "Saikiran Kandhi", "Shaik Afroz", "Venkat", "Jithendra reddy",
    "Bhavana Lanka", "Sravanthi Chapram", "B. Shrineeth Reddy",
    "Shreya Singh", "Tharuni Vallepi", "Saumya Lailamony",
    "Monisha", "Vijay Sai",
    "Ramya Lingaraj", "Devarajan SM"
]

USER_EMAILS = {
    "Saumya Lailamony": "Saumya.Lailamony@svarappstech.com",
    "Tharuni Vallepi": "Tharuni.Vallepi@svarappstech.com",
    "Shreya Singh": "Shreya.Singh@svarappstech.com",
    "Bhavana Lanka": "Bhavana.lanka@svarappstech.com",
    "Monisha": "Monisha.krishnamurthy@svarappstech.com",
    "Jithendra reddy": "Jithendra.R@svarappstech.com",
    "Shaik Afroz": "Afroz.S@svarappstech.com",
    "Sravanthi Chapram": "Sravanthi.Chapram@svarappstech.com",
    "B. Shrineeth Reddy": "Shrineeth.R@svarappstech.com",
    "Saikiran Kandhi": "Saikiran.K@svarappstech.com",
    "Vijay Sai": "Vijay.Velugubantla@svarappstech.com",
    "Venkat": "Venkat.Goriparthi@svarappstech.com",
    "Ramya Lingaraj": "Ramya.Lingaraj@svarappstech.com",
    "Devarajan SM": "Devarajan.manickam@svarappstech.com"
}

TEAM_NAMES = [
    "Reactor Core", "Apex Sync", "Pixel Forge", "Zero Gravity", "Ignition Squad", "Adrenaline Cartel", 
    "Logic Pulse", "Node Builders", "Venom Lab", "Kinetic Forge", "Quantum Delivery", "Adrenaline Catalyst", 
    "Innovators’ Guild", "FutureMakers", "IdeaCatalysts", "SparkLab", "InsightSphere", "KnowledgeCrafters", 
    "DiscoveryHub", "ResearchNest", "ThinkTankers", "FusionWorks", "CollabInnovate", "NextGen Minds", 
    "Catalyst Crew", "Labyrinth of Ideas", "Prototype Pioneers", "The Experimenters’ Guild", "IdeaStormers", 
    "Odyssey R&D", "Aurora Minds.", "InnoForge", "ThinkLab", "IdeaMint", "BrainMatter", "NextCore", 
    "CodePulse", "SparkHub", "LogicNest", "ProtoPoint", "FusionX", "NexGen Lab", "Innovex", "R&D Squad", 
    "IdeaCell", "CoreShift", "PrimeMind", "TechBloom", "DeepThink", "MindSprint", "QuantumWorks", 
    "VisionCraft", "NovaMinds", "BlueLabs", "AlphaThink", "IdeaGrid.", "TecNovid", "Tadino", "C-fit", 
    "Futi", "SizFin", "Noviq", "Lumira", "Sartiq", "Ventari", "Aethos", "Xelera", "Zenvia", "Lussio", 
    "Omniq", "Valoria", "Kinetiq", "Fiora", "Syntheo", "Aurore", "Eleviq", "InnoSprint", "IdeaSprint", 
    "BuildStorm", "ProtoMinds", "SparkShift", "FutureCraft", "BrightEdge", "MindForge", "InnoWave", 
    "ThinkStack", "The Idea Arch", "LogicWorks", "The Solutionists", "ThinkCatalyst", "FutureGrid", 
    "MoonShot Makers", "MindSpark", "EdgeWorks", "Cognitive Sparks", "The Foundry", "Iterate & Elevate", 
    "Pro Tech", "Core Collective", "Smart Works", "Idea Foundry", "Smart Squad", "Innovation Circle", 
    "Impact Team", "Team Rise", "New Path", "Vision Works", "Innovators", "Growth Hub", "Progress Team", 
    "Creative Pulse", "Change Makers", "Innovation Unit", "Smart Group", "Tech Circle", "Pro Thinkers", 
    "Team Forward", "Mindful Opus", "Unified Ergon", "A2Z_WEDO", "1 4!ALL", "Northfold", "Nexus ops", 
    "Prime Synapse", "In-various", "Aegorin", "Nexforge", "Sfaira Infinite", "No Finis", "Corepath", 
    "Primevector", "Axislimes", "Clearframe", "Varipoint", "Infyline", "181 Soros", "NeuraX", "AetherAI", 
    "QuantumEdge", "NovaMind", "CyberFlux", "SparkMind AI", "TechNova", "Digital Nexus", "Hyperion Labs", 
    "Future Systems Group", "IntelliTech", "InfiAI", "MindMesh", "Brainwave", "DeepLogic", "ThinkAI", 
    "IncuMind", "Synapse Studio", "CoreTech Innovation", "TechOrbit", "PowerAI Nexus", "Cognitive CloudWorks", 
    "FlowMind Innovators", "PowerSynapse Squad", "Fusion", "Intelligence Team", "AI‑Driven Makers", 
    "CloudFlow Architects", "NeuraPower Collective", "IntelliPlatform Crew", "AutoCloud Pioneers", 
    "Power AI Digital Team", "Enterprise Intelligent Automation Council", "Enterprise Power Automation and AI Office (EPAI)", 
    "Global Power Automation and AI Board (GPAI)", "IntelliOps Crew", "IntelliPlatform Guild", "PowerSphere AI", 
    "AIFabricators", "NeuroPower Makers", "PowerBots Consortium", "AppForge Intelligence", "Digital Dynamos", 
    "Visioneers", "The Byte Brigade", "Power AI Pros", "Core Connect", "SyncUP Team", "NextWave", "InnovX", 
    "FutureForge", "Technova", "Dynamiq", "Infinitum", "Incubis", "Ignitia", "Pulseon", "Techspire", "PioneerX", 
    "Creatiq", "Imaginex", "Concepta", "Datavex", "Logicore", "Infinitiq", "Visionix", "Coreon", "Techvanta", 
    "InnoVortex", "NovaForge", "Thinkubator", "IgniteX", "IdeaFoundry", "VisionCraft", "QuantumHive", "NeoGenesis", 
    "InnoCore", "MindForge", "FutureNest", "NovaThink", "AetherWorks", "Nexora", "Evolvex", "OriginPoint", 
    "Infinitum Forge", "HelixWorks", "FutureWeave", "Cognitiva", "Zentrix", "Neovex", "Quantro", "Virex", "Axion", 
    "Orbix", "Fluxa", "Kinetiq", "Xelion", "Ultrix", "NULL_STATE", "8HZ", "D E A D _ B I T", "ISO_CHROME", 
    "PRISM_RIOT", "Ambiance 1.0", "Object / 001", "Protocol 28", "Signal & Salt", "Cold Start", "NOISE FLOOR", 
    "RAW INPUT", "OFF GRID", "T-MINUS", "PAPER THIN", "28°_STUDIO.", "Hello Team.", "The Glitch.", "ROOM_204.", 
    "H Y P E R _ S O L E.", "C Y P H E R _ S I N."
]

USER_SUGGESTIONS = {
    # (Truncated for brevity, all mapping logic remains)
    "Ramya Lingaraj": [],
    "Devarajan SM": []
}

# ==========================================
# 4. CALLBACK FUNCTIONS
# ==========================================
def update_email():
    """Auto-fills email when name changes"""
    name = st.session_state.user_name
    if name in USER_EMAILS:
        st.session_state.user_email = USER_EMAILS[name]
    else:
        st.session_state.user_email = ""

def submit_vote():
    """Handles submission"""
    # 1. Get Values
    name = st.session_state.user_name
    email = st.session_state.user_email
    
    # Retrieve selection using dynamic key
    dynamic_key = f"team_select_{st.session_state.form_id}"
    teams = st.session_state.get(dynamic_key, [])
    
    # 2. Timer Check
    if not global_config["is_active"] or (global_config["end_time"] and time.time() > global_config["end_time"]):
        st.session_state.submission_error = "⚠️ Submission window closed."
        return

    # 3. Validation
    if name == "Select identity..." or not email:
        st.session_state.submission_error = "❌ Identity Required."
        return

    if not teams:
        st.session_state.submission_error = "❌ No Targets Selected. Pick at least one."
        return

    if not re.match(r"^[a-zA-Z0-9_.+-]+@svarappstech\.com$", email):
        st.session_state.submission_error = "❌ Invalid Email Domain."
        return

    # 4. Duplicate Check (Local)
    if email.strip().lower() in st.session_state.submitted_emails:
        st.session_state.submission_error = "❌ You have already submitted."
        return

    # 5. Transmission
    try:
        payload = {
            ENTRY_EMAIL: email,
            ENTRY_NAME: name,
            ENTRY_MAGIC: teams
        }
        
        # Send to Google
        requests.post(GOOGLE_FORM_URL, data=payload, timeout=5)
        
        # 6. Success Actions
        st.session_state.submitted_emails.add(email.strip().lower())
        
        # MAGIC FIX: Increment ID to destroy old widget and spawn a new one
        st.session_state.form_id += 1 
        
        st.session_state.success_flag = True
        st.session_state.submission_error = None
        
    except Exception as e:
        st.session_state.submission_error = f"Transmission Error: {e}"

# ==========================================
# 5. ADMIN CONTROLS
# ==========================================
with st.sidebar:
    st.header("Admin Access")
    admin_pw = st.text_input("Password", type="password")
    
    if admin_pw == "admin123":
        st.success("Authorized")
        st.markdown("---")
        
        # TIMER
        new_duration = st.number_input("Minutes", min_value=1, value=10, step=1)
        col_start, col_stop = st.columns(2)
        with col_start:
            if st.button("Start / Reset"):
                global_config["end_time"] = time.time() + (new_duration * 60)
                global_config["is_active"] = True
                st.rerun()
        with col_stop:
            if st.button("Stop"):
                global_config["is_active"] = False
                global_config["end_time"] = None
                st.rerun()

        st.markdown("---")
        
        # FORCE REFRESH
        if st.button("🔄 Force Refresh Dashboard"):
            st.rerun()
            
        # LOCAL DATA RESET
        if st.button("🧹 Clear Local Data"):
            st.session_state.submitted_emails = set()
            st.session_state.success_flag = False
            st.session_state.submission_error = None
            st.session_state.form_id += 1 # Reset form
            st.success("Local history cleared.")
            time.sleep(1)
            st.rerun()

# ==========================================
# 6. WATCHDOG / TIMER
# ==========================================
st.title("Identity Intel")
st.caption("Choose your team name wisely")

@st.fragment(run_every=1)
def timer_status_panel():
    current_is_active = global_config["is_active"]
    current_end_time = global_config["end_time"]
    time_left = (current_end_time - time.time()) if current_end_time else 0
    real_time_is_open = current_is_active and (time_left > 0)
    
    # Sync Main App State
    if real_time_is_open != st.session_state.last_known_is_open:
        st.session_state.last_known_is_open = real_time_is_open
        st.rerun()

    if real_time_is_open:
        mins, secs = divmod(int(time_left), 60)
        timer_text = f"{mins:02d}:{secs:02d}"
        st.markdown(f"""
        <div style="background-color:#e6fffa;padding:15px;border-radius:8px;border-left:5px solid #00bfa5;text-align:center;margin-bottom:20px;">
            <div style="font-size:14px;color:#444;font-weight:bold;">TIME REMAINING</div>
            <div style="font-size:32px;font-weight:800;color:#00796b;font-family:monospace;">{timer_text}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⛔ **TIME UP! Submissions Closed.**")

timer_status_panel()

# ==========================================
# 7. MAIN APP LOGIC
# ==========================================
is_open = st.session_state.last_known_is_open

if st.session_state.success_flag:
    st.toast("✅ Submitted successfully!", icon="🎉")
    st.session_state.success_flag = False

if st.session_state.submission_error:
    st.error(st.session_state.submission_error)
    st.session_state.submission_error = None

col_name, col_email = st.columns(2)
with col_name:
    st.selectbox(
        "Operative Name", 
        options=USER_NAMES, 
        disabled=not is_open, 
        key="user_name", 
        on_change=update_email
    )
with col_email:
    st.text_input(
        "Corporate Email", 
        placeholder="agent@svarappstech.com", 
        disabled=True, 
        key="user_email"
    )

# Filter suggestions
current_user = st.session_state.user_name
forbidden = USER_SUGGESTIONS.get(current_user, [])
available_teams = [t for t in TEAM_NAMES if t not in forbidden]

# Import
with st.expander("Bulk Import"):
    pasted_data = st.text_area("Paste Data", height=100, disabled=not is_open)
    if st.button("Process Data", disabled=not is_open):
        if current_user == "Select identity...":
            st.warning("Please select your name first.")
        elif pasted_data:
            clean_allowed = {t.strip().lower(): t for t in available_teams}
            matched_lines = []
            for line in pasted_data.replace('\r', '\n').split('\n'):
                cl = line.strip().lower()
                if clean_line and clean_line in clean_allowed: matched_lines.append(clean_allowed[cl])
            
            # Apply to CURRENT form ID
            current_key = f"team_select_{st.session_state.form_id}"
            if current_key in st.session_state:
                st.session_state[current_key] = list(set(st.session_state[current_key] + matched_lines))
            else:
                st.session_state[current_key] = matched_lines
            st.rerun()

# Selection
st.markdown("### Target Selection")
# DYNAMIC KEY - Prevents State Collision
dynamic_key = f"team_select_{st.session_state.form_id}"

st.multiselect(
    "Combobox Search",
    options=available_teams,
    key=dynamic_key,
    label_visibility="collapsed",
    placeholder="Search manually or review imported targets...",
    disabled=not is_open
)

st.write("")
if is_open:
    st.button("Submit Selections", type="primary", use_container_width=True, on_click=submit_vote)
else:
    st.button("⛔ Submission Closed", disabled=True, use_container_width=True)

st.divider()

# ==========================================
# 8. LIVE DASHBOARD (PURE SHEET DATA)
# ==========================================
@st.fragment(run_every=10)
def live_dashboard():
    st.markdown("### Live Leaderboard")

    try:
        # 1. READ GOOGLE SHEET
        df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
        
        # 2. VALIDATE EMPTINESS
        # Empty file or just headers means 0 votes
        if df.empty or len(df.columns) < 4:
            server_votes_list = []
        else:
            magic_column = df.columns[3]
            # Check if all rows in the voting column are NaN/Empty
            if df[magic_column].isnull().all():
                server_votes_list = []
            else:
                all_votes_series = df[magic_column].dropna().astype(str)
                server_votes_list = all_votes_series.str.split(',').explode().str.strip().tolist()

        # 3. DISPLAY
        if server_votes_list:
            df_combined = pd.DataFrame(server_votes_list, columns=['Designation'])
            vote_counts = df_combined['Designation'].value_counts()
            
            col_sort, col_slider = st.columns([1, 1])
            with col_sort:
                sort_order = st.selectbox("Sort By:", ["Most Votes", "Alphabetical"])
            with col_slider:
                top_n = st.slider("Display Top:", 5, 100, 30, 5)

            vote_counts = vote_counts.head(top_n)
            
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
            
            dynamic_height = max(300, len(df_plot) * 35)
            fig.update_layout(
                height=dynamic_height,
                bargap=0.35,
                xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Total Votes"),
                yaxis=dict(title=""),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0),
                font=dict(color="#0F172A")
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No votes logged yet.")

    except Exception as e:
        # Only show error if it's NOT an empty file error
        if "No columns to parse" in str(e) or "EmptyDataError" in str(e):
             st.info("No votes logged yet.")
        else:
             st.warning("Syncing with HQ...")

live_dashboard()
