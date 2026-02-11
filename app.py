import streamlit as st
import requests

# --- GOOGLE FORM CONFIGURATION ---
# Replace with your actual Form POST URL
GOOGLE_FORM_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT1iV4125NZgmskENeTvn71zt7gF7X8gy260UXQruoh5Os4WfxLgWWoGiMWv18jYlWcck6dlzHUq9X5/pub?output=csv"

# Replace with your specific Form Entry IDs (You find these via "Get pre-filled link")
ENTRY_EMAIL = "entry.111111" 
ENTRY_NAME = "entry.222222"
ENTRY_MAGIC = "entry.333333" 

# --- DATA: USERS & TEAMS ---
USER_NAMES = [
    "Saikiran Kandhi", "Shaik Afroz", "Venkat", "Jithendra reddy", 
    "Bhavana Lanka", "Sravanthi Chapram", "B. Shrineeth Reddy", 
    "Shreya Singh", "Tharuni Vallepi", "Saumya Lailamony", "Monisha", "Vijay Sai"
]

# The complete list of team names you provided
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

# --- MAPPING: USER TO THEIR SUGGESTIONS ---
# IMPORTANT: You must map the rest of the names here based on your Excel sheet!
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

# --- PAGE SETUP & PREMIUM CSS ---
st.set_page_config(page_title="Identity Intel", page_icon="✨", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    .stApp { background-color: #f4f5f7; font-family: 'Inter', sans-serif; }
    .main-card {
        background-color: white; padding: 40px; border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); margin-top: 20px;
    }
    div.stButton > button {
        background-color: #0f172a; color: white; border-radius: 8px;
        padding: 12px 24px; font-weight: 600; width: 100%; border: none;
        transition: all 0.2s ease; margin-top: 20px;
    }
    div.stButton > button:hover { background-color: #334155; color: white; }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'selections' not in st.session_state:
    st.session_state.selections = []

# --- LAYOUT ALIGNMENT ---
spacer_left, main_col, spacer_right = st.columns([1, 2, 1])

with main_col:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #0f172a;'>The Identity Intel</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 30px;'>Secure your target selections below.</p>", unsafe_allow_html=True)
    
    # ROW 1: Identity
    col_name, col_email = st.columns(2)
    with col_name:
        user_name = st.selectbox("Your Name", options=["Select your name..."] + USER_NAMES)
    with col_email:
        user_email = st.text_input("Your Email", placeholder="agent@intel.com")
        
    # --- EXCLUSION LOGIC ---
    # Calculate which teams this specific user is allowed to vote for
    forbidden_teams = USER_SUGGESTIONS.get(user_name, [])
    allowed_teams = [team for team in TEAM_NAMES if team not in forbidden_teams]
    
    # Clean up existing selections if the user changes their name
    st.session_state.selections = [t for t in st.session_state.selections if t in allowed_teams]

    st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 25px 0;'>", unsafe_allow_html=True)

    # ROW 2: Bulk Import
    st.markdown("#### 1. Bulk Import (Optional)")
    st.caption("Paste a column from Excel here. Your own suggestions will be automatically ignored.")
    pasted_data = st.text_area("Paste Data", height=100, label_visibility="collapsed")
    
    if st.button("Process Pasted Data"):
        if user_name == "Select your name...":
            st.warning("Please select your name first so we can filter your suggestions.")
        elif pasted_data:
            # Only allow names that are in the master list AND not suggested by this user
            lines = [line.strip() for line in pasted_data.split('\n') if line.strip() in allowed_teams]
            st.session_state.selections = list(set(st.session_state.selections + lines))
            st.success(f"Processed targets. Excluded {len(pasted_data.split()) - len(lines)} invalid/self-suggested items.")
            st.rerun()

    # ROW 3: Target Selection
    st.markdown("<br>#### 2. Target Selection", unsafe_allow_html=True)
    st.caption("Search manually, or review imported targets.")
    
    # The dropdown now ONLY shows the `allowed_teams`
    final_selections = st.multiselect(
        "Combobox Search",
        options=allowed_teams,
        default=st.session_state.selections,
        label_visibility="collapsed",
        placeholder="Type to search and select targets..."
    )
    
    st.session_state.selections = final_selections

    # ROW 4: Submission
    if st.button("SUBMIT SELECTIONS"):
        if user_name == "Select your name..." or not user_email:
            st.error("Please provide both your Name and Email.")
        elif not final_selections:
            st.error("Please select at least one target.")
        else:
            with st.spinner("Transmitting to database..."):
                payload = {
                    ENTRY_EMAIL: user_email,
                    ENTRY_NAME: user_name,
                    ENTRY_MAGIC: ", ".join(final_selections)
                }
                try:
                    response = requests.post(GOOGLE_FORM_URL, data=payload)
                    if response.status_code == 200:
                        st.success("Data secured and transmitted successfully!")
                        st.balloons()
                        st.session_state.selections = [] # Clear form
                    else:
                        st.error("Submission failed. Check your Form URL and Entry IDs.")
                except Exception as e:
                    st.error(f"Network error: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)
