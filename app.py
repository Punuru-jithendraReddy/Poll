import streamlit as st
import requests

# --- GOOGLE FORM CONFIGURATION ---
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse"
ENTRY_EMAIL = "entry.111111" 
ENTRY_NAME = "entry.222222"
ENTRY_MAGIC = "entry.333333" 

# --- DATA: USERS & TEAMS ---
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

# --- PAGE SETUP & LUXURY CSS ---
st.set_page_config(page_title="Identity Intel", page_icon="⚜️", layout="wide")

st.markdown("""
<style>
    /* Luxury Typography: Playfair for Headings, Montserrat for UI text */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Playfair+Display:wght@500;700&display=swap');
    
    .stApp { 
        background-color: #08080a; 
        font-family: 'Montserrat', sans-serif; 
        color: #e0e0e0;
    }
    
    /* The main glowing card */
    .main-card {
        background: linear-gradient(145deg, #131316 0%, #0d0d10 100%);
        padding: 50px; 
        border-radius: 20px;
        border: 1px solid #2a2824;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 40px rgba(212, 175, 55, 0.05);
        margin-top: 20px;
    }
    
    /* Luxury Headings */
    .luxury-title {
        font-family: 'Playfair Display', serif;
        color: #d4af37; /* Metallic Gold */
        text-align: center;
        letter-spacing: 3px;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    .luxury-subtitle {
        text-align: center; 
        color: #8b8b8d; 
        font-weight: 300;
        letter-spacing: 1px;
        margin-bottom: 40px;
    }
    .section-header {
        font-family: 'Playfair Display', serif;
        color: #d4af37;
        font-size: 1.3rem;
        border-bottom: 1px solid #2a2824;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Input Field Styling (Dark & Sleek) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #0b0b0d !important;
        color: #e0e0e0 !important;
        border: 1px solid #33312b !important;
        border-radius: 8px !important;
        font-family: 'Montserrat', sans-serif;
    }
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 0 1px #d4af37 !important;
    }
    
    /* Multiselect Tags (Gold Chips) */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1a1814;
        border: 1px solid #d4af37;
        color: #d4af37;
        font-weight: 500;
    }
    .stMultiSelect [data-baseweb="tag"] span {
        color: #d4af37;
    }

    /* Premium Gold Button */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #aa8822 100%);
        color: #000 !important;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 600;
        letter-spacing: 1.5px;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.15);
        text-transform: uppercase;
    }
    div.stButton > button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.3);
        background: linear-gradient(135deg, #e5c158 0%, #bb9933 100%);
    }
    
    hr { border-color: #2a2824; }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'selections' not in st.session_state:
    st.session_state.selections = []

# --- LAYOUT ALIGNMENT ---
spacer_left, main_col, spacer_right = st.columns([1, 2, 1])

with main_col:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    # Elegant Titles
    st.markdown("<div class='luxury-title'>THE IDENTITY INTEL</div>", unsafe_allow_html=True)
    st.markdown("<div class='luxury-subtitle'>Secure your target selections</div>", unsafe_allow_html=True)
    
    # ROW 1: Identity
    col_name, col_email = st.columns(2)
    with col_name:
        user_name = st.selectbox("OPERATIVE NAME", options=["Select identity..."] + USER_NAMES)
    with col_email:
        user_email = st.text_input("ENCRYPTED EMAIL", placeholder="agent@intel.com")
        
    # --- EXCLUSION LOGIC ---
    forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
    allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]
    
    # Clean up selections if name changes
    st.session_state.selections = [t for t in st.session_state.selections if t in allowed_teams]

    # ROW 2: Bulk Import
    st.markdown("<div class='section-header'>I. Bulk Data Import</div>", unsafe_allow_html=True)
    st.caption("Paste a column from Excel here. System will automatically filter formatting and self-suggestions.")
    pasted_data = st.text_area("Paste Data", height=120, label_visibility="collapsed", placeholder="Paste Excel rows here...")
    
    if st.button("Authenticate & Process Data"):
        if user_name == "Select identity...":
            st.warning("⚠️ Please select your operative name first to apply correct filters.")
        elif pasted_data:
            # BUG FIX: Robust matching to ignore Excel \r carriage returns and capitalization errors
            clean_allowed = {t.strip().lower(): t for t in allowed_teams}
            matched_lines = []
            
            # Replace Excel \r with standard \n, then split
            raw_lines = pasted_data.replace('\r', '\n').split('\n')
            
            for line in raw_lines:
                clean_line = line.strip().lower()
                if clean_line and clean_line in clean_allowed:
                    # Append the perfectly capitalized version from the master list
                    matched_lines.append(clean_allowed[clean_line])
            
            # Combine new matches with existing selections (removing duplicates)
            st.session_state.selections = list(set(st.session_state.selections + matched_lines))
            
            total_processed = len([l for l in raw_lines if l.strip()])
            st.success(f"✓ Authentication complete: Successfully matched {len(matched_lines)} out of {total_processed} submitted targets.")
            st.rerun()

    # ROW 3: Target Selection (Fixed the Markdown rendering issue here)
    st.markdown("<div class='section-header'>II. Final Target Roster</div>", unsafe_allow_html=True)
    st.caption("Review authenticated imports below, or search manually.")
    
    final_selections = st.multiselect(
        "Combobox Search",
        options=allowed_teams,
        default=st.session_state.selections,
        label_visibility="collapsed",
        placeholder="Type to add targets..."
    )
    st.session_state.selections = final_selections

    # ROW 4: Submission
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EXECUTE SELECTIONS"):
        if user_name == "Select identity..." or not user_email:
            st.error("Authentication Error: Please provide both Name and Email.")
        elif not final_selections:
            st.error("Requirement Error: Please select at least one target to proceed.")
        else:
            with st.spinner("Establishing secure uplink to database..."):
                payload = {
                    ENTRY_EMAIL: user_email,
                    ENTRY_NAME: user_name,
                    ENTRY_MAGIC: ", ".join(final_selections)
                }
                try:
                    response = requests.post(GOOGLE_FORM_URL, data=payload)
                    if response.status_code == 200:
                        st.success("Log confirmed. Targets secured successfully.")
                        st.balloons()
                        st.session_state.selections = [] 
                    else:
                        st.error("Uplink failed. Check your configuration URLs.")
                except Exception as e:
                    st.error(f"Network termination: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)
