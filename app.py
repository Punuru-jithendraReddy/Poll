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
# 2. MASTER DATA
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

USER_SUGGESTIONS = {
    "Saikiran Kandhi": ["Reactor Core","Apex Sync","Pixel Forge","Zero Gravity","Ignition Squad","Adrenaline Cartel","Logic Pulse","Node Builders","Venom Lab","Kinetic Forge","Quantum Delivery","Adrenaline Catalyst"],
    "Shaik Afroz": ["Innovators’ Guild","FutureMakers","IdeaCatalysts","SparkLab","InsightSphere","KnowledgeCrafters","DiscoveryHub","ResearchNest","ThinkTankers","FusionWorks","CollabInnovate","NextGen Minds","Catalyst Crew","Labyrinth of Ideas","Prototype Pioneers","The Experimenters’ Guild","IdeaStormers","Odyssey R&D","Aurora Minds."],
    "Venkateswara Rao": ["InnoForge","ThinkLab","IdeaMint","BrainMatter","NextCore","CodePulse","SparkHub","LogicNest","ProtoPoint","FusionX","NexGen Lab","Innovex","R&D Squad","IdeaCell","CoreShift","PrimeMind","TechBloom","DeepThink","MindSprint","QuantumWorks","VisionCraft","NovaMinds","BlueLabs","AlphaThink","IdeaGrid."],
    "Jithendra Reddy": ["TecNovid","Tadino","C-fit","Futi","SizFin","Noviq","Lumira","Sartiq","Ventari","Aethos","Xelera","Zenvia","Lussio","Omniq","Valoria","Kinetiq","Fiora","Syntheo","Aurore","Eleviq"],
    "Bhavana Lanka": ["InnoSprint","IdeaSprint","BuildStorm","ProtoMinds","SparkShift","FutureCraft","BrightEdge","MindForge","InnoWave","ThinkStack","The Idea Arch","LogicWorks","The Solutionists","ThinkCatalyst","FutureGrid","MoonShot Makers","MindSpark","EdgeWorks","Cognitive Sparks","The Foundry","Iterate & Elevate"],
    "Sravanthi C H": ["Pro Tech","Core Collective","Smart Works","Idea Foundry","Smart Squad","Innovation Circle","Impact Team","Team Rise","New Path","Vision Works","Innovators","Growth Hub","Progress Team","Creative Pulse","Change Makers","Innovation Unit","Smart Group","Tech Circle","Pro Thinkers","Team Forward"],
    "Shrineeth Reddy B": ["Mindful Opus","Unified Ergon","A2Z_WEDO","1 4!ALL","Northfold","Nexus ops","Prime Synapse","In-various","Aegorin","Nexforge","Sfaira Infinite","No Finis","Corepath","Primevector","Axislimes","Clearframe","Varipoint","Infyline","181 Soros"],
    "Shreya singh": ["NeuraX","AetherAI","QuantumEdge","NovaMind","CyberFlux","SparkMind AI","TechNova","Digital Nexus","Hyperion Labs","Future Systems Group","IntelliTech","InfiAI","MindMesh","Brainwave","DeepLogic","ThinkAI","IncuMind","Synapse Studio","CoreTech Innovation","TechOrbit"],
    "Tharuni": ["PowerAI Nexus","Cognitive CloudWorks","FlowMind Innovators","PowerSynapse Squad","Fusion","Intelligence Team","AI-Driven Makers","CloudFlow Architects","NeuraPower Collective","IntelliPlatform Crew","AutoCloud Pioneers","Power AI Digital Team","Enterprise Intelligent Automation Council","Enterprise Power Automation and AI Office (EPAI)","Global Power Automation and AI Board (GPAI)","IntelliOps Crew","IntelliPlatform Guild","PowerSphere AI","AIFabricators","NeuroPower Makers","PowerBots Consortium","AppForge Intelligence","Digital Dynamos","Visioneers","The Byte Brigade","Power AI Pros","Core Connect","SyncUP Team"],
    "Saumya L": ["NextWave","InnovX","FutureForge","Technova","Dynamiq","Infinitum","Incubis","Ignitia","Pulseon","Techspire","PioneerX","Creatiq","Imaginex","Concepta","Datavex","Logicore","Infinitiq","Visionix","Coreon","Techvanta"],
    "Monisha K": ["InnoVortex","NovaForge","Thinkubator","IgniteX","IdeaFoundry","VisionCraft","QuantumHive","NeoGenesis","InnoCore","MindForge","FutureNest","NovaThink","AetherWorks","Nexora","Evolvex","OriginPoint","Infinitum Forge","HelixWorks","FutureWeave","Cognitiva","Zentrix","Neovex","Quantro","Virex","Axion","Orbix","Fluxa","Kinetiq","Xelion","Ultrix"],
    "Velugubantla Vijay Sai": ["NULL_STATE","8HZ","D E A D _ B I T","ISO_CHROME","PRISM_RIOT","Ambiance 1.0","Object / 001","Protocol 28","Signal & Salt","Cold Start","NOISE FLOOR","RAW INPUT","OFF GRID","T-MINUS","PAPER THIN","28°_STUDIO.","Hello Team.","The Glitch.","ROOM_204.","H Y P E R _ S O L E.","C Y P H E R _ S I N."]
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

# ==========================================
# 3. GLOBAL STATE & CONFIG
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="centered")

@st.cache_resource
def get_global_config():
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
if "last_known_is_open" not in st.session_state:
    st.session_state.last_known_is_open = False

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
# 5. TIMER WATCHDOG
# ==========================================
st.title("Identity Intel")
st.caption("Choose your team name wisely")

@st.fragment(run_every=1)
def timer_status_panel():
    current_is_active = global_config["is_active"]
    current_end_time = global_config["end_time"]
    time_left = (current_end_time - time.time()) if current_end_time else 0
    real_time_is_open = current_is_active and (time_left > 0)
    
    # Sync with main app logic if state changes
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

# --- INPUT FORM ---
col_name, col_email = st.columns(2)

with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES, disabled=not is_open)

with col_email:
    current_email = USER_EMAILS.get(user_name, "") if user_name != "Select identity..." else ""
    user_email = st.text_input("Corporate Email", value=current_email, disabled=True)

forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]
st.session_state.team_select = [t for t in st.session_state.team_select if t in allowed_teams]

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

st.markdown("### Target Selection")
final_selections = st.multiselect(
    "Combobox", options=allowed_teams, key="team_select", label_visibility="collapsed",
    placeholder="Select teams...", disabled=not is_open
)

# --- SMART SUBMISSION LOGIC ---
def submit_data_smartly(url, email, name, magic_data):
    # Headers to mimic a browser (Crucial for 400 errors)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": url
    }
    
    # ATTEMPT 1: Standard List (For Checkboxes)
    try:
        payload = {ENTRY_EMAIL: email, ENTRY_NAME: name, ENTRY_MAGIC: magic_data}
        response = requests.post(url, data=payload, headers=headers, timeout=8)
        response.raise_for_status()
        return True, "Success"
    except requests.exceptions.HTTPError as e:
        # If 400 Bad Request, it might be that the form expects a single string string, not a list
        if response.status_code == 400:
            try:
                # ATTEMPT 2: Join with commas (For Text/Paragraph fields)
                joined_data = ", ".join(magic_data)
                payload_retry = {ENTRY_EMAIL: email, ENTRY_NAME: name, ENTRY_MAGIC: joined_data}
                response = requests.post(url, data=payload_retry, headers=headers, timeout=8)
                response.raise_for_status()
                return True, "Success (Retry Mode)"
            except Exception as e2:
                return False, f"Form Rejected Data (400). Check if you selected too many items or if email is blocked. Error: {e2}"
        return False, f"HTTP Error: {e}"
    except Exception as e:
        return False, f"Connection Error: {e}"

st.write("")
if is_open:
    if st.button("Submit Selections", type="primary", use_container_width=True):
        
        if not global_config["is_active"] or (global_config["end_time"] and time.time() > global_config["end_time"]):
            st.error("⚠️ Submission window closed just now.")
            time.sleep(2)
            st.rerun()
        elif user_name == "Select identity..." or not user_email:
            st.error("Name and Email required.")
        elif not final_selections:
            st.error("Select at least one target.")
        else:
            t_mail = user_email.strip().lower()
            
            # Check Duplicates Locally
            if t_mail in st.session_state.submitted_emails:
                st.error("Already submitted (Local Check).")
            else:
                success, msg = submit_data_smartly(GOOGLE_FORM_URL, user_email, user_name, final_selections)
                
                if success:
                    st.session_state.submitted_emails.add(t_mail)
                    st.session_state.recent_submissions.extend(final_selections)
                    st.session_state.team_select = []
                    st.session_state.success_flag = True
                    st.rerun()
                else:
                    st.error(f"❌ Submission Failed: {msg}")
else:
    st.button("⛔ Submission Closed", disabled=True, use_container_width=True)

st.divider()

# ==========================================
# 7. LIVE DASHBOARD (AUTO-REFRESHING)
# ==========================================
# This fragment refreshes ONLY the graph every 3 seconds
# ensuring "live updates without fail"
@st.fragment(run_every=3)
def live_dashboard():
    st.markdown("### Live Leaderboard")
    try:
        # 1. Fetch CSV (Silent Fail Proof)
        try:
            df = pd.read_csv(f"{GOOGLE_SHEET_CSV_URL}&t={int(time.time())}", on_bad_lines='skip')
            if not df.empty and len(df.columns) >= 4:
                # Column 3 is typically the Magic Data in standard form layout
                # Adjust index if your sheet layout is different
                s_votes = df[df.columns[3]].dropna().astype(str).str.split(',').explode().str.strip().tolist()
            else: 
                s_votes = []
        except:
            s_votes = []
        
        # 2. Merge with Local Session (Instant Updates)
        total = s_votes + st.session_state.recent_submissions
        
        if total:
            vc = pd.DataFrame(total, columns=['D']).value_counts().reset_index()
            vc.columns = ['Designation', 'Votes']
            
            # Sort: Highest Votes on Top
            vc = vc.sort_values('Votes', ascending=True).tail(20) # Tail of Ascending = Highest at end (Top of graph)
            
            fig = px.bar(vc, x='Votes', y='Designation', orientation='h', text='Votes')
            fig.update_traces(marker_color='#FF4B4B', textposition='outside')
            fig.update_layout(height=max(300, len(vc)*35), yaxis={'title':''}, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No votes recorded yet.")
            
    except Exception as e:
        st.warning("Dashboard syncing...")

live_dashboard()
