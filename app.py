import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px
import time
from datetime import datetime, timedelta

# ==========================================
# 1. SYSTEM CONFIGURATION
# ==========================================
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse"
ENTRY_EMAIL = "emailAddress"
ENTRY_NAME = "entry.1398544706"
ENTRY_MAGIC = "entry.921793836"

# Using the CSV export link
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"

# ADMIN CONFIGURATION
ADMIN_PASSWORD = "admin123"  # <--- CHANGE THIS PASSWORD

# ==========================================
# 2. MASTER DATA
# ==========================================
USER_NAMES = [
    "Saikiran Kandhi", "Shaik Afroz", "Venkat", "Jithendra reddy",
    "Bhavana Lanka", "Sravanthi Chapram", "B. Shrineeth Reddy",
    "Shreya Singh", "Tharuni Vallepi", "Saumya Lailamony",
    "Monisha", "Vijay Sai"
]

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
    "Saikiran Kandhi": ["Reactor Core","Apex Sync","Pixel Forge","Zero Gravity","Ignition Squad","Adrenaline Cartel","Logic Pulse","Node Builders","Venom Lab","Kinetic Forge","Quantum Delivery","Adrenaline Catalyst"],
    "Shaik Afroz": ["Innovators’ Guild","FutureMakers","IdeaCatalysts","SparkLab","InsightSphere","KnowledgeCrafters","DiscoveryHub","ResearchNest","ThinkTankers","FusionWorks","CollabInnovate","NextGen Minds","Catalyst Crew","Labyrinth of Ideas","Prototype Pioneers","The Experimenters’ Guild","IdeaStormers","Odyssey R&D","Aurora Minds."],
    "Venkat": ["InnoForge","ThinkLab","IdeaMint","BrainMatter","NextCore","CodePulse","SparkHub","LogicNest","ProtoPoint","FusionX","NexGen Lab","Innovex","R&D Squad","IdeaCell","CoreShift","PrimeMind","TechBloom","DeepThink","MindSprint","QuantumWorks","VisionCraft","NovaMinds","BlueLabs","AlphaThink","IdeaGrid."],
    "Jithendra reddy": ["TecNovid","Tadino","C-fit","Futi","SizFin","Noviq","Lumira","Sartiq","Ventari","Aethos","Xelera","Zenvia","Lussio","Omniq","Valoria","Kinetiq","Fiora","Syntheo","Aurore","Eleviq"],
    "Bhavana Lanka": ["InnoSprint","IdeaSprint","BuildStorm","ProtoMinds","SparkShift","FutureCraft","BrightEdge","MindForge","InnoWave","ThinkStack","The Idea Arch","LogicWorks","The Solutionists","ThinkCatalyst","FutureGrid","MoonShot Makers","MindSpark","EdgeWorks","Cognitive Sparks","The Foundry","Iterate & Elevate"],
    "Sravanthi Chapram": ["Pro Tech","Core Collective","Smart Works","Idea Foundry","Smart Squad","Innovation Circle","Impact Team","Team Rise","New Path","Vision Works","Innovators","Growth Hub","Progress Team","Creative Pulse","Change Makers","Innovation Unit","Smart Group","Tech Circle","Pro Thinkers","Team Forward"],
    "B. Shrineeth Reddy": ["Mindful Opus","Unified Ergon","A2Z_WEDO","1 4!ALL","Northfold","Nexus ops","Prime Synapse","In-various","Aegorin","Nexforge","Sfaira Infinite","No Finis","Corepath","Primevector","Axislimes","Clearframe","Varipoint","Infyline","181 Soros"],
    "Shreya Singh": ["NeuraX","AetherAI","QuantumEdge","NovaMind","CyberFlux","SparkMind AI","TechNova","Digital Nexus","Hyperion Labs","Future Systems Group","IntelliTech","InfiAI","MindMesh","Brainwave","DeepLogic","ThinkAI","IncuMind","Synapse Studio","CoreTech Innovation","TechOrbit"],
    "Tharuni Vallepi": ["PowerAI Nexus","Cognitive CloudWorks","FlowMind Innovators","PowerSynapse Squad","Fusion","Intelligence Team","AI-Driven Makers","CloudFlow Architects","NeuraPower Collective","IntelliPlatform Crew","AutoCloud Pioneers","Power AI Digital Team","Enterprise Intelligent Automation Council","Enterprise Power Automation and AI Office (EPAI)","Global Power Automation and AI Board (GPAI)","IntelliOps Crew","IntelliPlatform Guild","PowerSphere AI","AIFabricators","NeuroPower Makers","PowerBots Consortium","AppForge Intelligence","Digital Dynamos","Visioneers","The Byte Brigade","Power AI Pros","Core Connect","SyncUP Team"],
    "Saumya Lailamony": ["NextWave","InnovX","FutureForge","Technova","Dynamiq","Infinitum","Incubis","Ignitia","Pulseon","Techspire","PioneerX","Creatiq","Imaginex","Concepta","Datavex","Logicore","Infinitiq","Visionix","Coreon","Techvanta"],
    "Monisha": ["InnoVortex","NovaForge","Thinkubator","IgniteX","IdeaFoundry","VisionCraft","QuantumHive","NeoGenesis","InnoCore","MindForge","FutureNest","NovaThink","AetherWorks","Nexora","Evolvex","OriginPoint","Infinitum Forge","HelixWorks","FutureWeave","Cognitiva","Zentrix","Neovex","Quantro","Virex","Axion","Orbix","Fluxa","Kinetiq","Xelion","Ultrix"],
    "Vijay Sai": ["NULL_STATE","8HZ","D E A D _ B I T","ISO_CHROME","PRISM_RIOT","Ambiance 1.0","Object / 001","Protocol 28","Signal & Salt","Cold Start","NOISE FLOOR","RAW INPUT","OFF GRID","T-MINUS","PAPER THIN","28°_STUDIO.","Hello Team.","The Glitch.","ROOM_204.","H Y P E R _ S O L E.","C Y P H E R _ S I N."]
}

# ==========================================
# 3. PAGE SETUP & GLOBAL STATE
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="centered")

# Global Configuration Store (Shared across all users)
@st.cache_resource
def get_global_config():
    # Stores the absolute timestamp when the form closes
    return {"end_time": None, "is_active": False}

global_config = get_global_config()

# Session State Init
if "team_select" not in st.session_state:
    st.session_state.team_select = []
if "recent_submissions" not in st.session_state:
    st.session_state.recent_submissions = [] 
if "submitted_emails" not in st.session_state:
    st.session_state.submitted_emails = set()

# ==========================================
# ADMIN PANEL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("Admin Access")
    admin_pw = st.text_input("Password", type="password")
    
    if admin_pw == ADMIN_PASSWORD:
        st.success("Authorized")
        st.markdown("---")
        st.subheader("Timer Controls")
        
        # Determine current status
        now = time.time()
        time_remaining = 0
        if global_config["is_active"] and global_config["end_time"]:
            time_remaining = global_config["end_time"] - now
        
        # Display Status
        if time_remaining > 0:
            mins = int(time_remaining // 60)
            secs = int(time_remaining % 60)
            st.metric("Time Remaining", f"{mins}m {secs}s")
        else:
            st.metric("Status", "Stopped")

        # Controls
        col_start, col_stop = st.columns(2)
        
        with col_start:
            # START NEW TIMER
            new_duration = st.number_input("Minutes", min_value=1, value=10, step=1)
            if st.button("Start Timer"):
                global_config["end_time"] = time.time() + (new_duration * 60)
                global_config["is_active"] = True
                st.rerun()

        with col_stop:
            # STOP IMMEDIATELY
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("Stop/Reset"):
                global_config["is_active"] = False
                global_config["end_time"] = None
                st.rerun()
                
        st.markdown("---")
        # EXTEND TIMER
        extend_min = st.number_input("Extend by (mins)", min_value=1, value=5, step=1)
        if st.button("Extend Time"):
            if global_config["is_active"] and global_config["end_time"]:
                # If time expired, restart from now, else add to existing
                if time_remaining <= 0:
                     global_config["end_time"] = time.time() + (extend_min * 60)
                else:
                    global_config["end_time"] += (extend_min * 60)
                st.success(f"Extended by {extend_min} mins")
                st.rerun()
            else:
                st.error("Start timer first.")

# ==========================================
# BULK IMPORT LOGIC
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
st.caption("Choose your team name wisely")

# TIMER VISUALIZATION FOR USER
current_time = time.time()
is_submission_open = False
seconds_left = 0

if global_config["is_active"] and global_config["end_time"]:
    seconds_left = global_config["end_time"] - current_time
    if seconds_left > 0:
        is_submission_open = True
        # Calculate pretty time
        m, s = divmod(int(seconds_left), 60)
        st.info(f"⏳ **Submission Window Closing In:** {m} min {s} sec")
    else:
        st.error("⛔ **Submission Window Closed.**")
else:
    st.warning("⏸️ **Submissions are currently paused by Admin.**")

# --- FORM ---
col_name, col_email = st.columns(2)
with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES)
with col_email:
    user_email = st.text_input("Corporate Email", placeholder="agent@svarsppstech.com")

forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]

# Sync session state
st.session_state.team_select = [t for t in st.session_state.team_select if t in allowed_teams]

# Import Section
with st.expander("Bulk Import"):
    pasted_data = st.text_area("Paste Data", height=100)
    if st.button("Process Data"):
        if user_name == "Select identity...":
            st.warning("Please select your name first.")
        elif pasted_data:
            count = process_bulk_import(pasted_data, allowed_teams)
            st.success(f"Matched {count} targets.")
            st.rerun()

# Selection
st.markdown("### Target Selection")
final_selections = st.multiselect(
    "Combobox Search",
    options=allowed_teams,
    key="team_select",
    label_visibility="collapsed",
    placeholder="Search manually or review imported targets..."
)

# ==========================================
# SUBMISSION LOGIC (CONDITIONAL)
# ==========================================
# Only show Submit button if timer is valid
if is_submission_open:
    if st.button("Submit Selections", type="primary"):
        if user_name == "Select identity..." or not user_email:
            st.error("Please provide Name and Email.")
        elif not final_selections:
            st.error("Please select at least one target.")
        elif not re.match(r"^[a-zA-Z0-9_.+-]+@svarsppstech\.com$", user_email):
            st.error("Invalid email. Only @svarsppstech.com emails are allowed.")
        else:
            # --- DUPLICATE CHECK START ---
            is_duplicate = False
            target_email = user_email.strip().lower()

            # 1. Local Check (Instant block if user just submitted)
            if target_email in st.session_state.submitted_emails:
                is_duplicate = True
            
            # 2. Server Check (Check Google Sheet)
            if not is_duplicate:
                try:
                    check_url = f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}"
                    df = pd.read_csv(check_url, on_bad_lines='skip')
                    df_string = df.astype(str).apply(lambda x: x.str.strip().str.lower())
                    if (df_string == target_email).any().any():
                        is_duplicate = True
                except:
                    pass
            
            # --- SUBMISSION START ---
            if is_duplicate:
                st.error("This email has already submitted.")
            else:
                payload = {
                    ENTRY_EMAIL: user_email,
                    ENTRY_NAME: user_name,
                    ENTRY_MAGIC: final_selections
                }
                
                try:
                    requests.post(GOOGLE_FORM_URL, data=payload, timeout=5)
                    st.session_state.submitted_emails.add(target_email)
                    st.session_state.recent_submissions.extend(final_selections)
                    st.success("Submission successful!")
                    st.session_state.team_select = [] # Clear form
                    st.rerun() # Refresh to show success and update graph
                except:
                    pass
else:
    # Button disabled state
    st.button("Submit Selections", disabled=True, help="Timer has expired or not started.")

st.divider()

# ==========================================
# 5. LIVE DASHBOARD (INSTANT)
# ==========================================
st.markdown("### Live Leaderboard")

try:
    df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
    
    if not df.empty and len(df.columns) >= 4:
        magic_column = df.columns[3]
        all_votes_series = df[magic_column].dropna().astype(str)
        server_votes_list = all_votes_series.str.split(',').explode().str.strip().tolist()
    else:
        server_votes_list = []

    total_votes_list = server_votes_list + st.session_state.recent_submissions
    
    if total_votes_list:
        df_combined = pd.DataFrame(total_votes_list, columns=['Designation'])
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

except:
    st.warning("Dashboard initializing...")
