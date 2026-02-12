import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px
import time

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="wide")

# ==========================================
# 2. GLOBAL STATE & CONFIG
# ==========================================
@st.cache_resource
def get_global_config():
    return {"end_time": None, "is_active": False}

global_config = get_global_config()

# Initialize Session State
if "team_select" not in st.session_state: st.session_state.team_select = []
if "recent_submissions" not in st.session_state: st.session_state.recent_submissions = [] 
if "submitted_emails" not in st.session_state: st.session_state.submitted_emails = set()
if "success_flag" not in st.session_state: st.session_state.success_flag = False
if "last_known_is_open" not in st.session_state: st.session_state.last_known_is_open = False

# ==========================================
# 3. MASTER DATA
# ==========================================
USER_NAMES = [
    "Saumya L", "Tharuni", "Shreya singh", "Bhavana Lanka", "Monisha K", 
    "Jithendra Reddy", "Shaik Afroz", "Sravanthi C H", "Shrineeth Reddy B", 
    "Saikiran Kandhi", "Velugubantla Vijay Sai", "Venkateswara Rao"
]

USER_EMAILS = {
    "Saumya L": "Saumya.Lailamony@svarappstech.com",
    "Tharuni": "Tharuni.Vallepi@svarappstech.com",
    "Shreya singh": "Shreya.Singh@svarappstech.com",
    "Bhavana Lanka": "Bhavana.lanka@svarappstech.com",
    "Monisha K": "Monisha.krishnamurthy@svarappstech.com",
    "Jithendra Reddy": "Jithendra.R@svarappstech.com",
    "Shaik Afroz": "Afroz.S@svarappstech.com",
    "Sravanthi C H": "Sravanthi.Chapram@svarappstech.com",
    "Shrineeth Reddy B": "Shrineeth.R@svarappstech.com",
    "Saikiran Kandhi": "Saikiran.K@svarappstech.com",
    "Velugubantla Vijay Sai": "Vijay.Velugubantla@svarappstech.com",
    "Venkateswara Rao": "Venkat.Goriparthi@svarappstech.com"
}

# Standard Team List
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

# ==========================================
# 4. ADMIN & CONFIG
# ==========================================
with st.sidebar:
    st.header("Admin Access")
    admin_pw = st.text_input("Password", type="password")
    is_admin = (admin_pw == "admin123")
    
    if is_admin:
        st.success("Access Granted")
        st.divider()
        st.subheader("⚙️ Form Settings")
        
        # DEFAULT IDs - CHANGED TO THE ONES FROM YOUR LINK
        conf_form_url = st.text_input("Form URL", value="https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse")
        conf_sheet_url = st.text_input("Sheet CSV URL", value="https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv")
        
        st.markdown("**Entry IDs (From your pre-filled link)**")
        conf_entry_name = st.text_input("Name ID", value="entry.1398544706")
        conf_entry_magic = st.text_input("Team ID", value="entry.921793836")
        
        st.divider()
        st.subheader("⏱️ Timer Controls")
        new_duration = st.number_input("Minutes", min_value=1, value=10, step=1)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Start Timer"):
                global_config["end_time"] = time.time() + (new_duration * 60)
                global_config["is_active"] = True
                st.rerun()
        with c2:
            if st.button("Stop Timer"):
                global_config["is_active"] = False
                global_config["end_time"] = None
                st.rerun()
    else:
        # HARDCODED DEFAULTS (So it works without Admin login)
        conf_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse"
        conf_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"
        conf_entry_name = "entry.1398544706"
        conf_entry_magic = "entry.921793836"

# ==========================================
# 5. TIMER WATCHDOG
# ==========================================
st.title("Identity Intel")
st.caption("Operative Selection Dashboard")

@st.fragment(run_every=1)
def timer_panel():
    if global_config["is_active"] and global_config["end_time"]:
        remaining = global_config["end_time"] - time.time()
        is_open = remaining > 0
        
        if is_open:
            mins, secs = divmod(int(remaining), 60)
            st.markdown(f"""
            <div style="background:#e3f2fd;padding:15px;border-radius:10px;text-align:center;border:1px solid #90caf9;">
                <h3 style="margin:0;color:#1565c0;">⏳ {mins:02d}:{secs:02d}</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("⛔ MISSION WINDOW CLOSED")
            if st.session_state.last_known_is_open: # Only rerun on state change
                st.session_state.last_known_is_open = False
                st.rerun()
                
        # Sync state
        if is_open != st.session_state.last_known_is_open:
            st.session_state.last_known_is_open = is_open
            st.rerun()

timer_panel()

# ==========================================
# 6. MAIN APPLICATION
# ==========================================
is_open = st.session_state.last_known_is_open

if st.session_state.success_flag:
    st.toast("✅ Mission Data Uploaded Successfully!", icon="🚀")
    st.session_state.success_flag = False

# Inputs
c_name, c_email = st.columns(2)
with c_name:
    user_name = st.selectbox("Operative Identity", ["Select identity..."] + USER_NAMES, disabled=not is_open)
with c_email:
    # Auto-fill email but DO NOT SEND IT TO GOOGLE to avoid 400 Error
    current_email = USER_EMAILS.get(user_name, "")
    user_email = st.text_input("Encrypted Channel (Email)", value=current_email, disabled=True)

# Team Selection
st.markdown("### Target Acquisition")
final_selections = st.multiselect(
    "Select Targets", options=TEAM_NAMES, key="team_select", 
    label_visibility="collapsed", placeholder="Select targets...", disabled=not is_open
)

# Bulk Import
with st.expander("Bulk Data Upload"):
    pasted_data = st.text_area("Paste List", height=100, disabled=not is_open)
    if st.button("Process Bulk Data", disabled=not is_open):
        clean_allowed = {t.strip().lower(): t for t in TEAM_NAMES}
        matched = []
        if pasted_data:
            for line in pasted_data.replace('\r', '\n').split('\n'):
                cl = line.strip().lower()
                if cl in clean_allowed: matched.append(clean_allowed[cl])
            st.session_state.team_select = list(set(st.session_state.team_select + matched))
            st.rerun()

# --- CLASSIC SUBMISSION LOGIC (The Fix) ---
def submit_classic(url, name_id, name_val, team_id, team_list):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 1. Base Payload (Name)
    payload = {name_id: name_val}
    
    # 2. Add Teams (The Request library handles lists correctly for checkboxes)
    # This sends entry.123=TeamA&entry.123=TeamB
    payload[team_id] = team_list
    
    # 3. NO EMAIL in payload (Fixes 400 error if form doesn't collect emails)
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True, "Success"
    except requests.exceptions.HTTPError as e:
        return False, f"Google Rejected (400). Error: {e}"
    except Exception as e:
        return False, f"Connection Error: {e}"

st.write("")
if is_open:
    if st.button("EXECUTE MISSION (SUBMIT)", type="primary", use_container_width=True):
        if user_name == "Select identity...":
            st.error("Identity Verification Failed: Select Name.")
        elif not final_selections:
            st.error("No Targets Selected.")
        else:
            success, msg = submit_classic(
                conf_form_url,
                conf_entry_name, user_name,
                conf_entry_magic, final_selections
            )
            
            if success:
                st.session_state.submitted_emails.add(user_email)
                st.session_state.recent_submissions.extend(final_selections)
                st.session_state.team_select = []
                st.session_state.success_flag = True
                st.rerun()
            else:
                st.error(f"❌ Transmission Failed: {msg}")
else:
    st.button("⛔ MISSION WINDOW CLOSED", disabled=True, use_container_width=True)

st.divider()

# ==========================================
# 7. LIVE DASHBOARD
# ==========================================
@st.fragment(run_every=2)
def live_dashboard():
    st.markdown("### Live Leaderboard")
    try:
        # Load Data
        df = pd.read_csv(f"{conf_sheet_url}&t={int(time.time())}", on_bad_lines='skip')
        
        # Process Google Sheet Data
        sheet_votes = []
        if not df.empty and len(df.columns) >= 3: # Ensure enough columns
            # Column index 2 is usually the 3rd column (Team Selection)
            # Adjust if your sheet is different
            col_idx = 2 if len(df.columns) > 2 else -1
            if col_idx != -1:
                sheet_votes = df.iloc[:, col_idx].dropna().astype(str).str.split(',').explode().str.strip().tolist()

        # Merge with Local Session
        total_votes = sheet_votes + st.session_state.recent_submissions
        
        if total_votes:
            # Count & Sort
            vc = pd.DataFrame(total_votes, columns=['Team']).value_counts().reset_index()
            vc.columns = ['Team', 'Votes']
            
            # Sort Descending (Highest on Top)
            # In Plotly Horizontal Bar, the bottom of the list is the top of the chart.
            # So we sort Ascending (Small -> Large) so Large is at the "end" (Top).
            vc = vc.sort_values('Votes', ascending=True).tail(15)
            
            fig = px.bar(vc, x='Votes', y='Team', orientation='h', text='Votes')
            fig.update_traces(marker_color='#FF4B4B', textposition='outside')
            fig.update_layout(
                height=max(400, len(vc)*40), 
                yaxis={'title':''}, 
                xaxis={'title':''},
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Awaiting Data...")
            
    except Exception:
        # Silent fail for dashboard to prevent UI flickering
        pass

live_dashboard()
