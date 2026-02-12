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
# 2. GLOBAL STATE & CONFIG
# ==========================================
@st.cache_resource
def get_global_config():
    return {"end_time": None, "is_active": False}

global_config = get_global_config()

# Local session state initialization
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

# (Truncated for brevity, assuming standard lists as before)
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
# 4. ADMIN & CONFIGURATION SIDEBAR
# ==========================================
with st.sidebar:
    st.header("Admin Access")
    admin_pw = st.text_input("Password", type="password")
    
    is_admin = (admin_pw == "admin123")
    
    if is_admin:
        st.success("Authorized")
        st.divider()
        st.subheader("⚠️ Form Configuration")
        
        # --- CONFIGURABLE IDs ---
        conf_form_url = st.text_input("Form URL", value="https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse")
        conf_sheet_url = st.text_input("Sheet CSV URL", value="https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv")
        
        st.markdown("**Entry IDs (From your URL)**")
        conf_entry_name = st.text_input("Name ID", value="entry.1398544706")
        conf_entry_magic = st.text_input("Team Selection ID", value="entry.921793836")
        
        # --- FIX FOR 400 ERROR ---
        st.divider()
        st.markdown("**Does your Google Form collect emails?**")
        st.caption("If your form setting 'Collect email addresses' is OFF, uncheck this box. Otherwise, the form will reject the data.")
        conf_send_email = st.checkbox("Send Email to Google?", value=False) # DEFAULT FALSE TO FIX CRASH
        
        if conf_send_email:
            conf_entry_email = st.text_input("Email ID (e.g. emailAddress)", value="emailAddress")
        else:
            conf_entry_email = None

        st.divider()
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
                
    else:
        # Defaults if not logged in (User cannot see config)
        conf_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdd5OKJTG3E6k37eV9LbeXPxgSV7G8ONiMgnxoWunkn_hgY8Q/formResponse"
        conf_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"
        conf_entry_name = "entry.1398544706"
        conf_entry_magic = "entry.921793836"
        conf_entry_email = None # Default to None (Don't send email)
        conf_send_email = False

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
    current_email = USER_EMAILS.get(user_name, "") if user_name != "Select identity..." else ""
    user_email = st.text_input("Corporate Email", value=current_email, disabled=True)

# Suggestions Logic 
USER_SUGGESTIONS = {} 
forbidden_teams = [] 
allowed_teams = TEAM_NAMES 
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

# --- SMART SUBMISSION LOGIC (ROBUST RETRY) ---
def submit_data_smartly(url, email_id, email_val, name_id, name_val, magic_id, magic_val, should_send_email):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
        "Referer": url
    }
    
    # Payload Base: Name Only
    payload = {
        name_id: name_val
    }
    
    # Only add email if configured to do so
    if should_send_email and email_id:
        payload[email_id] = email_val
    
    # ATTEMPT 1: Checkbox Style (List)
    try:
        # Add magic data as list (requests handles this as entry=A&entry=B)
        payload[magic_id] = magic_val 
        response = requests.post(url, data=payload, headers=headers, timeout=8)
        response.raise_for_status()
        return True, "Success"
    except requests.exceptions.HTTPError as e:
        # If 400, it might be the format
        if e.response.status_code == 400:
            try:
                # ATTEMPT 2: String Style (For Text/Paragraph Questions)
                payload[magic_id] = ", ".join(magic_val)
                response = requests.post(url, data=payload, headers=headers, timeout=8)
                response.raise_for_status()
                return True, "Success (Retry Mode)"
            except:
                pass # Fail through to return original error
        return False, f"Google Rejected Data (400). ERROR: Verify IDs. Is Email Config Correct? (Error: {e})"
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
            
            if t_mail in st.session_state.submitted_emails:
                st.error("Already submitted (Local Check).")
            else:
                # USE CONFIGURABLE IDs
                success, msg = submit_data_smartly(
                    conf_form_url, 
                    conf_entry_email, user_email, 
                    conf_entry_name, user_name, 
                    conf_entry_magic, final_selections,
                    conf_send_email # Pass the flag from config
                )
                
                if success:
                    st.session_state.submitted_emails.add(t_mail)
                    st.session_state.recent_submissions.extend(final_selections)
                    st.session_state.team_select = []
                    st.session_state.success_flag = True
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
                    if is_admin:
                        st.warning("Admin Tip: Uncheck 'Send Email to Google' in the sidebar if your form is anonymous.")
else:
    st.button("⛔ Submission Closed", disabled=True, use_container_width=True)

st.divider()

# ==========================================
# 7. LIVE DASHBOARD (AUTO-REFRESHING)
# ==========================================
@st.fragment(run_every=3)
def live_dashboard():
    st.markdown("### Live Leaderboard")
    try:
        try:
            # Use Configurable Sheet URL
            df = pd.read_csv(f"{conf_sheet_url}&t={int(time.time())}", on_bad_lines='skip')
            if not df.empty and len(df.columns) >= 4:
                # Assuming standard layout, column 3 (index 3, which is 4th col) is usually the answer
                s_votes = df[df.columns[3]].dropna().astype(str).str.split(',').explode().str.strip().tolist()
            else: 
                s_votes = []
        except:
            s_votes = []
        
        total = s_votes + st.session_state.recent_submissions
        
        if total:
            vc = pd.DataFrame(total, columns=['D']).value_counts().reset_index()
            vc.columns = ['Designation', 'Votes']
            vc = vc.sort_values('Votes', ascending=True).tail(20) 
            
            fig = px.bar(vc, x='Votes', y='Designation', orientation='h', text='Votes')
            fig.update_traces(marker_color='#FF4B4B', textposition='outside')
            fig.update_layout(height=max(300, len(vc)*35), yaxis={'title':''}, plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No votes recorded yet.")
            
    except Exception as e:
        st.warning("Dashboard syncing...")

live_dashboard()
