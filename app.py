import streamlit as st
import os
from groq import Groq
import PyPDF2
import json
import random
import time

# --- 1. SETUP & SECRET KEY ---
st.set_page_config(
    page_title="Vibranium Node | AI Tutor",
    page_icon="🐾",
    layout="wide"
)

# 🔴🔴🔴 PASTE YOUR API KEY HERE 🔴🔴🔴
# Replace the text inside the quotes with your actual Groq API Key
GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 

# --- 2. THE BLACK PANTHER THEME (CSS) ---
st.markdown("""
    <style>
    /* MAIN BACKGROUND */
    .stApp {
        background-color: #0e1117;
        background-image: linear-gradient(315deg, #0e1117 0%, #1a1a2e 74%);
        color: #e0e0e0;
        font-family: 'Courier New', monospace;
    }
    
    /* VIBRANIUM GLOW BUTTONS */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4b0082 0%, #7b2cbf 100%);
        color: white;
        border: 1px solid #9d4edd;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px #7b2cbf;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #9d4edd;
        border-color: white;
    }

    /* SCROLLING TICKER (MARQUEE) */
    .ticker-wrap {
        width: 100%;
        background-color: #121212;
        border-top: 2px solid #7b2cbf;
        border-bottom: 2px solid #7b2cbf;
        overflow: hidden;
        height: 40px;
        line-height: 40px;
        margin-bottom: 20px;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        padding-right: 100%;
        animation: ticker 30s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        padding: 0 2rem;
        font-size: 14px;
        color: #00d4ff; /* Neon Blue */
        text-shadow: 0 0 5px #00d4ff;
    }
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }

    /* CUSTOM HEADERS */
    h1 {
        color: white;
        text-shadow: 0 0 10px #7b2cbf;
        font-family: 'Arial Black', sans-serif;
    }
    h3 {
        color: #9d4edd;
        border-left: 5px solid #00d4ff;
        padding-left: 10px;
    }

    /* RADIO BUTTONS (HUD STYLE) */
    .stRadio > div {
        background-color: #1f1f2e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3c3c54;
    }
    
    /* SUCCESS MESSAGES */
    .stSuccess {
        background-color: #064e3b;
        color: #6ee7b7;
        border: 1px solid #059669;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE RUNNING TICKER (MARQUEE) ---
quotes = [
    "WAKANDA FOREVER 🙅🏾‍♂️",
    "SYSTEM STATUS: ONLINE. VIBRANIUM LEVELS: STABLE.",
    "KNOWLEDGE IS POWER. REVISION IS KEY.",
    "THE PANTHER NEVER FREEZES.",
    "GROQ API CONNECTION: ENCRYPTED.",
    "SHURI AI PROTOCOLS: ENGAGED.",
    "TODAY'S MISSION: ACE THE EXAM.",
    "I NEVER FREEZE. - T'CHALLA"
]
ticker_html = f"""
<div class="ticker-wrap">
<div class="ticker">
    {''.join([f'<div class="ticker-item">{q}</div>' for q in quotes])}
</div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# --- 4. SIDEBAR (SECURITY CLEARANCE) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Wakanda_flag.svg/2560px-Wakanda_flag.svg.png", width=100)
    st.markdown("### 🔐 SECURITY CLEARANCE")
    
    # Replaced Input Box with a Cool Status Indicator
    if GROQ_API_KEY.startswith("gsk_"):
        st.success("ACCESS GRANTED: IDENTITY VERIFIED")
        st.caption("UPLINK ESTABLISHED VIA SECURE CHANNEL")
    else:
        st.error("⚠️ ACCESS DENIED: INVALID KEY")
        st.caption("Please configure API Key in source code.")
    
    st.markdown("---")
    st.markdown("### 🎛️ SIMULATION LEVEL")
    difficulty = st.select_slider("", options=["Novice", "Warrior", "King"])
    
    st.markdown("---")
    st.info("Network: Wakanda Mesh v3.3")

# --- 5. MAIN INTERFACE ---
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🐾")
with col2:
    st.title("THE VIBRANIUM NODE")
    st.caption("ADVANCED AI REVISION SYSTEM // POWERED BY GROQ LPU™")

# --- 6. LOGIC FUNCTIONS ---
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_quiz(text, difficulty):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""
    Role: You are Shuri, the genius princess of Wakanda. 
    Task: Create 5 tough multiple-choice questions from the notes provided.
    Difficulty: {difficulty}
    Tone: Encouraging but intellectual.
    
    Output JSON ONLY:
    [
        {{
            "question": "Question text",
            "options": ["A", "B", "C", "D"],
            "correct_index": 0,
            "explanation": "Explanation text"
        }}
    ]
    
    Notes: {text[:4000]}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, 
            response_format={"type": "json_object"} 
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        st.error(f"SYSTEM BREACH: {e}")
        return None

# --- 7. THE TERMINAL (FILE UPLOADER) ---
st.markdown("### 📂 UPLOAD MISSION DATA")
uploaded_file = st.file_uploader("Drop PDF File Here to Initiate Analysis", type=["pdf"])

# Session State Initialization
if 'quiz_data' not in st.session_state: st.session_state.quiz_data = None
if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
if 'score' not in st.session_state: st.session_state.score = 0

if uploaded_file and GROQ_API_KEY:
    if st.button("⚡ ACTIVATE VIBRANIUM PROCESSING"):
        with st.spinner("ACCESSING SHURI'S DATABASE..."):
            text = extract_text_from_pdf(uploaded_file)
            time.sleep(1) 
            response = generate_quiz(text, difficulty)
            if response:
                st.session_state.quiz_data = response.get('questions', response)
                st.session_state.user_answers = {}
                st.session_state.score = 0
                st.rerun()

# --- 8. THE QUIZ DISPLAY (HUD) ---
if st.session_state.quiz_data:
    st.markdown("---")
    st.markdown("## 🛡️ COMBAT SIMULATION ACTIVE")
    
    data = st.session_state.quiz_data
    if isinstance(data, list):
        correct_count = 0
        
        for i, q in enumerate(data):
            st.markdown(f"### // TARGET {i+1}: {q.get('question')}")
            
            options = q.get('options', [])
            val = st.radio(f"Select Strategy for Target {i+1}", options, key=f"q{i}", index=None)
            
            if val:
                st.session_state.user_answers[i] = val
                correct_option = options[q.get('correct_index', 0)]
                
                if val == correct_option:
                    st.success(f"✅ TARGET NEUTRALIZED. {q.get('explanation')}")
                    correct_count += 1
                else:
                    st.error(f"⚠️ SYSTEM ERROR. Correct Path: {correct_option}")
                    st.info(f"Analysis: {q.get('explanation')}")
            st.markdown("<br>", unsafe_allow_html=True)
            
        if len(st.session_state.user_answers) == len(data):
            score = (correct_count / len(data)) * 100
            if score == 100:
                st.balloons()
                st.markdown("## 👑 WAKANDA SALUTES YOU! (100%)")
            else:
                st.markdown(f"## 📊 MISSION REPORT: {int(score)}% EFFICIENCY")