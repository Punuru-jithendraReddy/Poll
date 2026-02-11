import streamlit as st
import requests

# ==========================================
# 1. GOOGLE FORM CONFIGURATION
# ==========================================
# Replace YOUR_FORM_ID_HERE with your actual form ID
GOOGLE_FORM_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?output=csv"

# The exact hooks for your specific form
ENTRY_EMAIL = "emailAddress"   # Google's default keyword for the built-in email field
ENTRY_NAME = "entry.1398544706"    # REPLACE THIS with your 1st unique number (Name dropdown)
ENTRY_MAGIC = "entry.921793836"   # REPLACE THIS with your 2nd unique number (Target selection)

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
    "Saikiran Kandhi": [
        "Reactor Core",
        "Apex Sync",
        "Pixel Forge",
        "Zero Gravity",
        "Ignition Squad",
        "Adrenaline Cartel",
        "Logic Pulse",
        "Node Builders",
        "Venom Lab",
        "Kinetic Forge",
        "Quantum Delivery",
        "Adrenaline Catalyst"
    ],
    "Shaik Afroz": [
        "Innovators’ Guild",
        "FutureMakers",
        "IdeaCatalysts",
        "SparkLab",
        "InsightSphere",
        "KnowledgeCrafters",
        "DiscoveryHub",
        "ResearchNest",
        "ThinkTankers",
        "FusionWorks",
        "CollabInnovate",
        "NextGen Minds",
        "Catalyst Crew",
        "Labyrinth of Ideas",
        "Prototype Pioneers",
        "The Experimenters’ Guild",
        "IdeaStormers",
        "Odyssey R&D",
        "Aurora Minds."
    ],
    "Venkat": [
        "InnoForge",
        "ThinkLab",
        "IdeaMint",
        "BrainMatter",
        "NextCore",
        "CodePulse",
        "SparkHub",
        "LogicNest",
        "ProtoPoint",
        "FusionX",
        "NexGen Lab",
        "Innovex",
        "R&D Squad",
        "IdeaCell",
        "CoreShift",
        "PrimeMind",
        "TechBloom",
        "DeepThink",
        "MindSprint",
        "QuantumWorks",
        "VisionCraft",
        "NovaMinds",
        "BlueLabs",
        "AlphaThink",
        "IdeaGrid."
    ],
    "Jithendra reddy": [
        "TecNovid",
        "Tadino",
        "C-fit",
        "Futi",
        "SizFin",
        "Noviq",
        "Lumira",
        "Sartiq",
        "Ventari",
        "Aethos",
        "Xelera",
        "Zenvia",
        "Lussio",
        "Omniq",
        "Valoria",
        "Kinetiq",
        "Fiora",
        "Syntheo",
        "Aurore",
        "Eleviq"
    ],
    "Bhavana Lanka": [
        "InnoSprint",
        "IdeaSprint",
        "BuildStorm",
        "ProtoMinds",
        "SparkShift",
        "FutureCraft",
        "BrightEdge",
        "MindForge",
        "InnoWave",
        "ThinkStack",
        "The Idea Arch",
        "LogicWorks",
        "The Solutionists",
        "ThinkCatalyst",
        "FutureGrid",
        "MoonShot Makers",
        "MindSpark",
        "EdgeWorks",
        "Cognitive Sparks",
        "The Foundry",
        "Iterate & Elevate"
    ],
    "Sravanthi Chapram": [
        "Pro Tech",
        "Core Collective",
        "Smart Works",
        "Idea Foundry",
        "Smart Squad",
        "Innovation Circle",
        "Impact Team",
        "Team Rise",
        "New Path",
        "Vision Works",
        "Innovators",
        "Growth Hub",
        "Progress Team",
        "Creative Pulse",
        "Change Makers",
        "Innovation Unit",
        "Smart Group",
        "Tech Circle",
        "Pro Thinkers",
        "Team Forward"
    ],
    "B. Shrineeth Reddy": [
        "Mindful Opus",
        "Unified Ergon",
        "A2Z_WEDO",
        "1 4!ALL",
        "Northfold",
        "Nexus ops",
        "Prime Synapse",
        "In-various",
        "Aegorin",
        "Nexforge",
        "Sfaira Infinite",
        "No Finis",
        "Corepath",
        "Primevector",
        "Axislimes",
        "Clearframe",
        "Varipoint",
        "Infyline",
        "181 Soros"
    ],
    "Shreya Singh": [
        "NeuraX",
        "AetherAI",
        "QuantumEdge",
        "NovaMind",
        "CyberFlux",
        "SparkMind AI",
        "TechNova",
        "Digital Nexus",
        "Hyperion Labs",
        "Future Systems Group",
        "IntelliTech",
        "InfiAI",
        "MindMesh",
        "Brainwave",
        "DeepLogic",
        "ThinkAI",
        "IncuMind",
        "Synapse Studio",
        "CoreTech Innovation",
        "TechOrbit"
    ],
    "Tharuni Vallepi": [
        "PowerAI Nexus",
        "Cognitive CloudWorks",
        "FlowMind Innovators",
        "PowerSynapse Squad",
        "Fusion",
        "Intelligence Team",
        "AI-Driven Makers",
        "CloudFlow Architects",
        "NeuraPower Collective",
        "IntelliPlatform Crew",
        "AutoCloud Pioneers",
        "Power AI Digital Team",
        "Enterprise Intelligent Automation Council",
        "Enterprise Power Automation and AI Office (EPAI)",
        "Global Power Automation and AI Board (GPAI)",
        "IntelliOps Crew",
        "IntelliPlatform Guild",
        "PowerSphere AI",
        "AIFabricators",
        "NeuroPower Makers",
        "PowerBots Consortium",
        "AppForge Intelligence",
        "Digital Dynamos",
        "Visioneers",
        "The Byte Brigade",
        "Power AI Pros",
        "Core Connect",
        "SyncUP Team"
    ],
    "Saumya Lailamony": [
        "NextWave",
        "InnovX",
        "FutureForge",
        "Technova",
        "Dynamiq",
        "Infinitum",
        "Incubis",
        "Ignitia",
        "Pulseon",
        "Techspire",
        "PioneerX",
        "Creatiq",
        "Imaginex",
        "Concepta",
        "Datavex",
        "Logicore",
        "Infinitiq",
        "Visionix",
        "Coreon",
        "Techvanta"
    ],
    "Monisha": [
        "InnoVortex",
        "NovaForge",
        "Thinkubator",
        "IgniteX",
        "IdeaFoundry",
        "VisionCraft",
        "QuantumHive",
        "NeoGenesis",
        "InnoCore",
        "MindForge",
        "FutureNest",
        "NovaThink",
        "AetherWorks",
        "Nexora",
        "Evolvex",
        "OriginPoint",
        "Infinitum Forge",
        "HelixWorks",
        "FutureWeave",
        "Cognitiva",
        "Zentrix",
        "Neovex",
        "Quantro",
        "Virex",
        "Axion",
        "Orbix",
        "Fluxa",
        "Kinetiq",
        "Xelion",
        "Ultrix"
    ],
    "Vijay Sai": [
        "NULL_STATE",
        "8HZ",
        "D E A D _ B I T",
        "ISO_CHROME",
        "PRISM_RIOT",
        "Ambiance 1.0",
        "Object / 001",
        "Protocol 28",
        "Signal & Salt",
        "Cold Start",
        "NOISE FLOOR",
        "RAW INPUT",
        "OFF GRID",
        "T-MINUS",
        "PAPER THIN",
        "28°_STUDIO.",
        "Hello Team.",
        "The Glitch.",
        "ROOM_204.",
        "H Y P E R _ S O L E.",
        "C Y P H E R _ S I N."
    ]
}

# ==========================================
# 3. PAGE SETUP & ENTERPRISE UI
# ==========================================
st.set_page_config(page_title="Identity Intel", page_icon="🌐", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { 
        background-color: #f0f4f8; 
        font-family: 'Inter', sans-serif;
    }
    
    /* The white cloud dashboard card */
    .block-container {
        background-color: #ffffff;
        padding: 3rem 3rem 4rem 3rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-top: 3rem;
        margin-bottom: 3rem;
        border: 1px solid #e2e8f0;
    }

    header { visibility: hidden; }
    
    .app-title {
        color: #1e3a8a; font-size: 2.2rem; font-weight: 700;
        text-align: center; margin-bottom: 0.2rem;
    }
    .app-subtitle {
        color: #64748b; text-align: center; font-size: 1rem; margin-bottom: 2.5rem;
    }
    .section-header {
        color: #1e3a8a; font-weight: 600; font-size: 1.1rem;
        margin-top: 2rem; margin-bottom: 0.5rem;
        border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;
    }

    /* Inputs */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #ffffff !important; color: #0f172a !important;
        border: 1px solid #cbd5e1 !important; border-radius: 6px !important;
    }
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: #2563eb !important; box-shadow: 0 0 0 1px #2563eb !important;
    }
    
    /* Blue Multiselect Chips */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af;
    }
    .stMultiSelect [data-baseweb="tag"] span { color: #1e40af; }

    /* Blue Submit Button */
    div.stButton > button {
        background-color: #2563eb; color: #ffffff !important; border-radius: 6px;
        padding: 0.6rem 1.5rem; font-weight: 600; width: 100%; border: none;
        transition: all 0.2s ease; margin-top: 1.5rem;
    }
    div.stButton > button:hover { 
        background-color: #1d4ed8; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. APP LOGIC & LAYOUT
# ==========================================
if 'selections' not in st.session_state:
    st.session_state.selections = []

# Headers
st.markdown("<div class='app-title'>Identity Intel</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Secure Team Designation Portal</div>", unsafe_allow_html=True)

# ROW 1: Identity
col_name, col_email = st.columns(2)
with col_name:
    user_name = st.selectbox("Operative Name", options=["Select identity..."] + USER_NAMES)
with col_email:
    user_email = st.text_input("Corporate Email", placeholder="agent@intel.com")

# Apply self-suggestion exclusion rules
forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]
st.session_state.selections = [t for t in st.session_state.selections if t in allowed_teams]

# ROW 2: Bulk Import
st.markdown("<div class='section-header'>Bulk Data Import</div>", unsafe_allow_html=True)
pasted_data = st.text_area("Paste Data", height=100, label_visibility="collapsed", placeholder="Paste a column from Excel here...")

if st.button("Process Excel Data"):
    if user_name == "Select identity...":
        st.warning("Please select your name first to apply correct filters.")
    elif pasted_data:
        # Smart, case-insensitive match that ignores Excel carriage returns
        clean_allowed = {t.strip().lower(): t for t in allowed_teams}
        matched_lines = []
        raw_lines = pasted_data.replace('\r', '\n').split('\n')
        
        for line in raw_lines:
            clean_line = line.strip().lower()
            if clean_line and clean_line in clean_allowed:
                matched_lines.append(clean_allowed[clean_line])
        
        st.session_state.selections = list(set(st.session_state.selections + matched_lines))
        st.success(f"Successfully matched and authenticated {len(matched_lines)} targets.")
        st.rerun()

# ROW 3: Target Selection Box
st.markdown("<div class='section-header'>Target Selection</div>", unsafe_allow_html=True)
final_selections = st.multiselect(
    "Combobox Search",
    options=allowed_teams,
    default=st.session_state.selections,
    label_visibility="collapsed",
    placeholder="Search manually or review your imported targets..."
)
st.session_state.selections = final_selections

# ROW 4: Submission to Google Forms
if st.button("Submit Selections"):
    if user_name == "Select identity..." or not user_email:
        st.error("Authentication Error: Please provide both Name and Email.")
    elif not final_selections:
        st.error("Requirement Error: Please select at least one target.")
    else:
        with st.spinner("Establishing secure uplink to database..."):
            # Prepare data to send to Google Forms
            payload = {
                ENTRY_EMAIL: user_email,
                ENTRY_NAME: user_name,
                ENTRY_MAGIC: final_selections  # Passing as a list handles checkboxes perfectly!
            }
            try:
                response = requests.post(GOOGLE_FORM_URL, data=payload)
                if response.status_code == 200:
                    st.success("Log confirmed. Targets secured successfully.")
                    st.balloons()
                    st.session_state.selections = [] 
                else:
                    st.error(f"Uplink failed. Status Code: {response.status_code}. Check your Form URL and Entry IDs.")
            except Exception as e:
                st.error(f"Network termination: {e}")
