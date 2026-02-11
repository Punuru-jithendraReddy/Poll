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

# CRITICAL: Your published CSV link
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?gid=1388192502&single=true&output=csv"

# ==========================================
# 2. MASTER DATA
# ==========================================
USER_NAMES = [
    "Saikiran Kandhi", "Shaik Afroz", "Venkat", "Jithendra reddy", 
    "Bhavana Lanka", "Sravanthi Chapram", "B. Shrineeth Reddy", 
    "Shreya Singh", "Tharuni Vallepi", "Saumya Lailamony", "Monisha", "Vijay Sai"
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
    "Saikiran Kandhi": ["Reactor Core", "Apex Sync", "Pixel Forge", "Zero Gravity", "Ignition Squad"],
    "Shaik Afroz": ["FutureMakers", "IdeaCatalysts", "SparkLab", "InsightSphere"],
    "Venkat": [], "Jithendra reddy": [], "Bhavana Lanka": [], "Sravanthi Chapram": [], 
    "B. Shrineeth Reddy": [], "Shreya Singh": [], "Tharuni Vallepi": [], 
    "Saumya Lailamony": [], "Monisha": [], "Vijay Sai": []
}

# ==========================================
# 3. PAGE SETUP & HIGH-CONTRAST UI
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    /* Premium High-Contrast Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp { 
        background-color: #F8FAFC; /* Crisp Arctic Silver */
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }
    
    /* Modern Floating Glass Card */
    .block-container {
        background-color: #ffffff; 
        padding: 3.5rem 4rem 4.5rem 4rem !important; 
        border-radius: 20px; 
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08); 
        margin-top: 3rem; 
        margin-bottom: 3rem; 
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    header { visibility: hidden; }
    
    /* Vibrant Headings */
    .app-title { 
        color: #0F172A; /* Deep Slate */
        font-size: 2.6rem; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .app-subtitle { 
        color: #64748B; 
        text-align: center; 
        font-size: 1.05rem; 
        font-weight: 500;
        margin-bottom: 3rem; 
    }
    
    .section-header { 
        color: #0F172A; 
        font-weight: 700; 
        font-size: 1.25rem; 
        margin-top: 2.5rem; 
        margin-bottom: 0.8rem; 
        border-bottom: 2px solid #F1F5F9; 
        padding-bottom: 0.5rem; 
    }

    /* Crisp Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea { 
        background-color: #F8FAFC !important; 
        color: #0F172A !important; 
        border: 1px solid #E2E8F0 !important; 
        border-radius: 10px !important; 
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.01);
        padding: 0.5rem;
    }
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus { 
        border-color: #6366F1 !important; /* Vibrant Indigo Focus */
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important; 
        background-color: #FFFFFF !important;
    }
    
    /* Vibrant Multiselect Chips */
    .stMultiSelect [data-baseweb="tag"] { 
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); 
        border: 1px solid #C7D2FE; 
        color: #4338CA; 
        font-weight: 600;
        border-radius: 6px;
    }
    .stMultiSelect [data-baseweb="tag"] span { color: #4338CA; }

    /* Premium Gradient Button */
    div.stButton > button { 
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); /* Indigo to Purple Gradient */
        color: #ffffff !important; 
        border-radius: 10px; 
        padding: 0.8rem 1.5rem; 
        font-weight: 700; 
        width: 100%; 
        border: none; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
        margin-top: 2rem;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3), 0 4px 6px -2px rgba(99, 102, 241, 0.15);
    }
    div.stButton > button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.4), 0 10px 10px -5px rgba(99, 102, 241, 0.2); 
    }
    
    /* Slider Customization */
    .stSlider > div > div > div { background-color: #6366F1 !important; }
</style>
""", unsafe_allow_html=True)

if 'selections' not in st.session_state:
    st.session_state.selections = []

# ==========================================
# 4. PRIMARY APPLICATION
# ==========================================
st.markdown("<div class='app-title'>Identity Intel</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Secure Team Designation Portal</div>", unsafe_allow_html=True)

col_name, col_email = st.columns(2)
with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES)
with col_email:
    user_email = st.text_input("Corporate Email", placeholder="agent@intel.com")

forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]
st.session_state.selections = [t for t in st.session_state.selections if t in allowed_teams]

st.markdown("<div class='section-header'>Bulk Data Import</div>", unsafe_allow_html=True)
pasted_data = st.text_area("Paste Data", height=100, label_visibility="collapsed", placeholder="Paste a column from Excel here...")

if st.button("Process Excel Data"):
    if user_name == "Select identity...":
        st.warning("Please select your name first to apply correct filters.")
    elif pasted_data:
        clean_allowed = {t.strip().lower(): t for t in allowed_teams}
        matched_lines = []
        raw_lines = pasted_data.replace('\r', '\n').split('\n')
        for line in raw_lines:
            clean_line = line.strip().lower()
            if clean_line and clean_line in clean_allowed:
                matched_lines.append(clean_allowed[clean_line])
        st.session_state.selections = list(set(st.session_state.selections + matched_lines))
        st.success(f"Matched {len(matched_lines)} targets.")
        st.rerun()

st.markdown("<div class='section-header'>Target Selection</div>", unsafe_allow_html=True)
final_selections = st.multiselect("Combobox Search", options=allowed_teams, default=st.session_state.selections, label_visibility="collapsed", placeholder="Search manually or review your imported targets...")
st.session_state.selections = final_selections

# --- FAIL-SECURE SUBMISSION LOGIC ---
if st.button("Submit Selections"):
    if user_name == "Select identity..." or not user_email:
        st.error("Authentication Error: Please provide both Name and Email.")
    elif not final_selections:
        st.error("Requirement Error: Please select at least one target.")
    elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user_email):
        st.error("Validation Error: Please enter a valid corporate email address.")
    else:
        with st.spinner("Verifying credentials and checking database..."):
            can_submit = False
            
            try:
                df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
                if not df.empty:
                    df_string = df.astype(str).apply(lambda x: x.str.strip().str.lower())
                    target_email = user_email.strip().lower()
                    
                    if (df_string == target_email).any().any():
                        st.error(f"Access Denied: The identity '{user_email}' has already submitted a response.")
                    else:
                        can_submit = True 
                else:
                    can_submit = True 
            except Exception as e:
                st.error("Critical Error: Cannot connect to verification database. Check your internet connection or CSV link. System locked.")
            
            if can_submit:
                payload = {ENTRY_EMAIL: user_email, ENTRY_NAME: user_name, ENTRY_MAGIC: final_selections}
                try:
                    response = requests.post(GOOGLE_FORM_URL, data=payload)
                    if response.status_code == 200:
                        st.success("Log confirmed. Targets secured successfully.")
                        st.balloons()
                        st.session_state.selections = [] 
                    else:
                        st.error("Uplink failed. Check Form URL.")
                except Exception as e:
                    st.error(f"Network termination: {e}")

st.divider()

# ==========================================
# 5. LIVE DASHBOARD (WITH TOP N FILTER)
# ==========================================
st.markdown("<div class='section-header'>Live Leaderboard</div>", unsafe_allow_html=True)
st.caption("Live telemetry of designation targets.")

try:
    df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
    if not df.empty and len(df.columns) >= 4:
        magic_column = df.columns[3]
        all_votes = df[magic_column].dropna().astype(str)
        split_votes = all_votes.str.split(',').explode().str.strip()
        
        # --- NEW UI: SORTING AND TOP N SLIDER ---
        col_sort, col_slider = st.columns([1, 1])
        with col_sort:
            sort_order = st.selectbox("Sort Leaderboard By:", ["Most Votes", "Alphabetical"])
        with col_slider:
            # Lets the user slide from Top 5 to Top 100
            top_n = st.slider("Display Top:", min_value=5, max_value=100, value=30, step=5)
        
        # Calculate votes dynamically based on the slider!
        vote_counts = split_votes.value_counts().head(top_n)
        
        if not vote_counts.empty:
            df_plot = vote_counts.reset_index()
            df_plot.columns = ['Designation', 'Votes']
            
            if sort_order == "Most Votes":
                df_plot = df_plot.sort_values(by='Votes', ascending=True)
            else:
                df_plot = df_plot.sort_values(by='Designation', ascending=False)
            
            # Plotly Chart with vibrant Indigo bars
            fig = px.bar(
                df_plot, 
                x='Votes', 
                y='Designation', 
                orientation='h',       
                text='Votes',          
                color_discrete_sequence=["#4F46E5"] # Vibrant Indigo to match buttons
            )
            
            # Ensures spacing dynamically grows with the slider
            dynamic_height = max(350, len(df_plot) * 45)
            
            fig.update_layout(
                xaxis=dict(
                    rangemode='tozero',        
                    showgrid=True, 
                    gridcolor='#E2E8F0',
                    title="Total Votes",
                    dtick=1                    
                ), 
                yaxis=dict(title="", tickmode='linear'), 
                plot_bgcolor='rgba(0,0,0,0)',  
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=0),
                height=dynamic_height,
                font=dict(family="Plus Jakarta Sans", color="#0F172A")
            )
            
            fig.update_traces(textposition='outside', cliponaxis=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
        else:
            st.info("Awaiting initial telemetry. No votes logged yet.")
    else:
        st.info("Database is currently empty.")
except Exception as e:
    st.warning("Dashboard offline. Waiting for initial data synchronization.")
