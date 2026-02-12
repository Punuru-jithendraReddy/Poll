import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. SYSTEM CONFIGURATION
# ==========================================
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse"
ENTRY_EMAIL = "emailAddress"
ENTRY_NAME = "entry.1398544706"
ENTRY_MAGIC = "entry.921793836"
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"

ADMIN_PASSWORD = "admin123" 

# ==========================================
# 2. MASTER DATA (Your Lists)
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
# 3. GLOBAL STATE & CONFIG
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="centered")

@st.cache_resource
def get_global_config():
    # Store state in a mutable dictionary so all users share it
    return {"end_time": None, "is_active": False}

global_config = get_global_config()

# Local session state
if "team_select" not in st.session_state:
    st.session_state.team_select = []
if "recent_submissions" not in st.session_state:
    st.session_state.recent_submissions = [] 
if "submitted_emails" not in st.session_state:
    st.session_state.submitted_emails = set()
if "success_flag" not in st.session_state:
    st.session_state.success_flag = False

# ==========================================
# 4. ADMIN PANEL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("Admin Access")
    admin_pw = st.text_input("Password", type="password")
    
    if admin_pw == ADMIN_PASSWORD:
        st.success("Authorized")
        st.markdown("---")
        st.subheader("Timer Controls")
        
        # Admin controls update the global shared object directly
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
        extend_min = st.number_input("Extend by (mins)", min_value=1, value=5, step=1)
        if st.button("Extend Time"):
            if global_config["is_active"] and global_config["end_time"]:
                global_config["end_time"] += (extend_min * 60)
                st.success("Extended!")
                st.rerun()
            else:
                st.error("Timer not running.")

# ==========================================
# 5. SYNCHRONIZED TIMER (THE FIX)
# ==========================================
st.title("Identity Intel")
st.caption("Choose your team name wisely")

# This fragment runs EVERY 1 SECOND independently of the rest of the app.
# It ensures every user sees the exact same time and status.
@st.fragment(run_every=1)
def live_status_panel():
    is_active = global_config["is_active"]
    end_time = global_config["end_time"]
    
    if is_active and end_time:
        remaining = end_time - time.time()
        
        if remaining > 0:
            # Calculate m:s
            mins, secs = divmod(int(remaining), 60)
            timer_text = f"{mins:02d}:{secs:02d}"
            
            st.markdown(f"""
            <div style="
                background-color: #e6fffa; 
                padding: 15px; 
                border-radius: 8px; 
                border-left: 5px solid #00bfa5; 
                text-align: center; 
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 14px; color: #444; font-weight: bold; letter-spacing: 1px;">TIME REMAINING</div>
                <div style="font-size: 32px; font-weight: 800; color: #00796b; font-family: monospace;">{timer_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # If we were previously showing "Submission Closed", we need to unlock the UI
            # We do this by checking a local session state flag if needed, 
            # but usually the user will just see the timer.
            
        else:
            st.error("⛔ **TIME UP!**")
            # If time just ran out, we can trigger a rerun to lock inputs
            if remaining > -2: # Only rerun once right after expiry
                time.sleep(1)
                st.rerun()
    else:
        st.info("⏸️ **Submissions are currently PAUSED by Admin.**")

# Run the live panel
live_status_panel()

# ==========================================
# 6. MAIN APP LOGIC
# ==========================================

# Determine if inputs should be enabled based on global config
is_open = False
if global_config["is_active"] and global_config["end_time"]:
    if time.time() < global_config["end_time"]:
        is_open = True

# Check if a successful submission just happened
if st.session_state.success_flag:
    st.toast("✅ Submitted successfully!", icon="🎉")
    st.session_state.success_flag = False

# --- INPUT FORM ---
col_name, col_email = st.columns(2)
with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES, disabled=not is_open)
with col_email:
    user_email = st.text_input("Corporate Email", placeholder="agent@svarappstech.com", disabled=not is_open)

forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]
st.session_state.team_select = [t for t in st.session_state.team_select if t in allowed_teams]

# Import
with st.expander("Bulk Import"):
    pasted_data = st.text_area("Paste Data", height=100, disabled=not is_open)
    if st.button("Process Data", disabled=not is_open):
        clean_allowed = {t.strip().lower(): t for t in allowed_teams}
        matched = []
        if pasted_data:
            for line in pasted_data.replace('\r', '\n').split('\n'):
                cl = line.strip().lower()
                if cl in clean_allowed: matched.append(clean_allowed[cl])
            st.session_state.team_select = list(set(st.session_state.team_select + matched))
            st.success(f"Matched {len(matched)}.")
            st.rerun()

# Multiselect
st.markdown("### Target Selection")
final_selections = st.multiselect(
    "Combobox", options=allowed_teams, key="team_select", label_visibility="collapsed",
    placeholder="Select teams...", disabled=not is_open
)

# --- SUBMIT BUTTON ---
st.write("")
if is_open:
    if st.button("Submit Selections", type="primary", use_container_width=True):
        
        # Double check time on server side at moment of click
        if not global_config["is_active"] or time.time() > global_config["end_time"]:
            st.error("⚠️ Submission window closed just now.")
            time.sleep(2)
            st.rerun()
            
        elif user_name == "Select identity..." or not user_email:
            st.error("Name and Email required.")
        elif not final_selections:
            st.error("Select at least one target.")
        else:
            t_mail = user_email.strip().lower()
            if not re.match(r"^[a-z0-9_.+-]+@svarappstech\.com$", t_mail):
                 st.error("Invalid email. Only @svarappstech.com emails are allowed.")
            else:
                is_dup = False
                if t_mail in st.session_state.submitted_emails: is_dup = True
                
                if not is_dup:
                    try:
                        df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
                        if (df.astype(str).apply(lambda x: x.str.strip().str.lower()) == t_mail).any().any():
                            is_dup = True
                    except: pass 
                
                if is_dup:
                    st.error("Already submitted.")
                else:
                    try:
                        payload = {ENTRY_EMAIL: user_email, ENTRY_NAME: user_name, ENTRY_MAGIC: final_selections}
                        requests.post(GOOGLE_FORM_URL, data=payload, timeout=5)
                        
                        st.session_state.submitted_emails.add(t_mail)
                        st.session_state.recent_submissions.extend(final_selections)
                        st.session_state.team_select = []
                        st.session_state.success_flag = True 
                        st.rerun() 
                    except:
                        st.error("Network Error")
else:
    st.button("⛔ Submission Closed", disabled=True, use_container_width=True)

st.divider()

# ==========================================
# 7. DASHBOARD (Auto-refreshes with the app)
# ==========================================
st.markdown("### Live Leaderboard")
try:
    df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
    if not df.empty and len(df.columns) >= 4:
        s_votes = df[df.columns[3]].dropna().astype(str).str.split(',').explode().str.strip().tolist()
    else: s_votes = []
    
    total = s_votes + st.session_state.recent_submissions
    
    if total:
        vc = pd.DataFrame(total, columns=['D']).value_counts().reset_index()
        vc.columns = ['Designation', 'Votes']
        
        col_s, col_sl = st.columns(2)
        with col_s: sort = st.selectbox("Sort", ["Most Votes", "A-Z"])
        with col_sl: top = st.slider("Show", 5, 50, 20)
        
        if sort == "Most Votes":
             vc = vc.sort_values('Votes', ascending=True).tail(top)
        else:
             vc = vc.sort_values('Designation', ascending=False).tail(top)
        
        fig = px.bar(vc, x='Votes', y='Designation', orientation='h', text='Votes')
        fig.update_traces(marker_color='#FF4B4B', textposition='outside')
        fig.update_layout(height=max(300, len(vc)*35), yaxis={'title':''}, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No votes yet.")
except:
    pass
