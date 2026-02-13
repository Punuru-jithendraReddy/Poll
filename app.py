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
# 2. CONFIGURATION
# ==========================================
# Timer Config
@st.cache_resource
def get_global_config():
    return {"end_time": None, "is_active": False}

global_config = get_global_config()

# Basic Session State
if "team_select" not in st.session_state: st.session_state.team_select = []
if "submitted_emails" not in st.session_state: st.session_state.submitted_emails = set()
if "success_flag" not in st.session_state: st.session_state.success_flag = False
if "last_known_is_open" not in st.session_state: st.session_state.last_known_is_open = False

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
    "Vijay Sai": ["NULL_STATE","8HZ","D E A D _ B I T","ISO_CHROME","PRISM_RIOT","Ambiance 1.0","Object / 001","Protocol 28","Signal & Salt","Cold Start","NOISE FLOOR","RAW INPUT","OFF GRID","T-MINUS","PAPER THIN","28°_STUDIO.","Hello Team.","The Glitch.","ROOM_204.","H Y P E R _ S O L E.","C Y P H E R _ S I N."],
    "Ramya Lingaraj": [],
    "Devarajan SM": []
}

# ==========================================
# 4. ADMIN CONTROLS (Timer & RESET)
# ==========================================
with st.sidebar:
    st.header("Admin Access")
    admin_pw = st.text_input("Password", type="password")
    
    if admin_pw == "admin123":
        st.success("Authorized")
        st.markdown("---")
        st.subheader("Controls")
        
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

        # FORCE REFRESH
        st.markdown("---")
        if st.button("🔄 Force Refresh Dashboard"):
            st.rerun()

# ==========================================
# 5. WATCHDOG / TIMER
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
# 6. MAIN APP LOGIC
# ==========================================
is_open = st.session_state.last_known_is_open

if st.session_state.success_flag:
    st.toast("✅ Submitted successfully!", icon="🎉")
    st.session_state.success_flag = False

col_name, col_email = st.columns(2)
with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES, disabled=not is_open)
with col_email:
    current_email = USER_EMAILS.get(user_name, "")
    user_email = st.text_input("Corporate Email", value=current_email, placeholder="agent@svarsppstech.com", disabled=True)

forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]

# Sync session state
st.session_state.team_select = [t for t in st.session_state.team_select if t in allowed_teams]

# Import Section
with st.expander("Bulk Import"):
    pasted_data = st.text_area("Paste Data", height=100, disabled=not is_open)
    if st.button("Process Data", disabled=not is_open):
        if user_name == "Select identity...":
            st.warning("Please select your name first.")
        elif pasted_data:
            clean_allowed = {t.strip().lower(): t for t in allowed_teams}
            matched_lines = []
            for line in pasted_data.replace('\r', '\n').split('\n'):
                clean_line = line.strip().lower()
                if clean_line and clean_line in clean_allowed:
                    matched_lines.append(clean_allowed[clean_line])
            
            st.session_state.team_select = list(set(st.session_state.team_select + matched_lines))
            st.success(f"Matched {len(matched_lines)} targets.")
            st.rerun()

# Selection
st.markdown("### Target Selection")
final_selections = st.multiselect(
    "Combobox Search",
    options=allowed_teams,
    key="team_select",
    label_visibility="collapsed",
    placeholder="Search manually or review imported targets...",
    disabled=not is_open
)

# ==========================================
# SUBMISSION LOGIC
# ==========================================
st.write("")
if is_open:
    if st.button("Submit Selections", type="primary", use_container_width=True):
        if not global_config["is_active"] or (global_config["end_time"] and time.time() > global_config["end_time"]):
            st.error("⚠️ Submission window closed just now.")
            time.sleep(2)
            st.rerun()
        elif user_name == "Select identity..." or not user_email:
            st.error("Please provide Name and Email.")
        elif not final_selections:
            st.error("Please select at least one target.")
        elif not re.match(r"^[a-zA-Z0-9_.+-]+@svarappstech\.com$", user_email):
             st.error("Invalid email. Only @svarappstech.com emails are allowed.")
        else:
            # --- DUPLICATE CHECK START ---
            is_duplicate = False
            target_email = user_email.strip().lower()

            if target_email in st.session_state.submitted_emails:
                is_duplicate = True
            
            # --- SUBMISSION ---
            if is_duplicate:
                st.error("This email has already submitted (Local Check).")
            else:
                payload = {
                    ENTRY_EMAIL: user_email,
                    ENTRY_NAME: user_name,
                    ENTRY_MAGIC: final_selections
                }
                
                try:
                    # 1. SEND DATA
                    requests.post(GOOGLE_FORM_URL, data=payload, timeout=5)
                    st.session_state.submitted_emails.add(target_email)
                    
                    # 2. SUCCESS & REFRESH
                    st.session_state.team_select = []
                    st.session_state.success_flag = True
                    st.rerun()
                except:
                    pass
else:
    st.button("⛔ Submission Closed", disabled=True, use_container_width=True)

st.divider()

# ==========================================
# 8. LIVE DASHBOARD (PURE READ - 10s REFRESH)
# ==========================================
@st.fragment(run_every=10)
def live_dashboard():
    st.markdown("### Live Leaderboard")

    try:
        # 1. READ GOOGLE SHEET DIRECTLY
        df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
        
        # 2. PARSE DATA
        if not df.empty and len(df.columns) >= 4:
            magic_column = df.columns[3]
            all_votes_series = df[magic_column].dropna().astype(str)
            server_votes_list = all_votes_series.str.split(',').explode().str.strip().tolist()
        else:
            server_votes_list = []

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

    except:
        # If network error, just wait for next 10s cycle
        st.warning("Syncing with HQ...")

live_dashboard()
