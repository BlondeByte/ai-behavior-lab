from email.utils import quote
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import requests
from datetime import datetime
import time

# 👇 ADD THIS LINE
load_dotenv()

st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0f0f1a, #05050a);
    color: #eaeaf0;
}

/* Title styling */
h1 {
    color: #c9b6ff;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background-color: rgba(255,255,255,0.02);
    border: 1px solid rgba(200,180,255,0.15);
    border-radius: 12px;
    padding: 12px;
}

/* Buttons */
button {
    background: linear-gradient(135deg, #7b5cff, #c9b6ff);
    color: black;
    border-radius: 10px;
    border: none;
    font-weight: 500;
}

/* Toggle */
[data-testid="stToggle"] {
    background-color: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 6px;
}

/* Subtle glow */
h1, h2, h3 {
    text-shadow: 0 0 8px rgba(201,182,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# 👇 MOVE FUNCTION HERE
def log_to_airtable(user_input, response, mode, result):
    from urllib.parse import quote

    if not AIRTABLE_TABLE_NAME:
        st.error("Missing Airtable table name")
        return

    table_name_encoded = quote(str(AIRTABLE_TABLE_NAME))

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name_encoded}"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "Prompt": user_input,
            "Response": response,
            "Mode": "Injection" if mode else "Normal",
            "Result": result,
            "Timestamp": datetime.now().isoformat()
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            st.success("Logged to Airtable ✅")
        else:
            st.error("Logging failed ❌")
    except Exception:
        st.error("Airtable connection error ❌")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = None

client = OpenAI(api_key=api_key)


AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
if not AIRTABLE_API_KEY:
    try:
        AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
    except:
        AIRTABLE_API_KEY = None


AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
if not AIRTABLE_BASE_ID:
    try:
        AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
    except:
        AIRTABLE_BASE_ID = None


AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
if not AIRTABLE_TABLE_NAME:
    try:
        AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]
    except:
        AIRTABLE_TABLE_NAME = None

st.markdown("""
<h1>🧪 AI Behavior Lab</h1>
<p style='color:#a8a8c0; margin-top:-10px;'>
Evaluate model robustness, prompt injection resistance, and behavioral drift.
</p>
""", unsafe_allow_html=True)

# First line (your current subtitle)

# 👇 ADD THIS HERE
st.markdown("""
<div style="
    border: 1px solid rgba(201,182,255,0.2);
    padding: 12px;
    border-radius: 12px;
    background: rgba(255,255,255,0.02);
">
<h4 style='margin-bottom:10px;'>🧬 Experiment Settings</h4>
</div>
""", unsafe_allow_html=True)

mode = st.toggle("Enable Prompt Injection Test Mode")
st.caption("Toggle adversarial testing to evaluate model robustness against malicious prompts.")

st.markdown("""
<div style="
    border: 1px solid rgba(201,182,255,0.2);
    padding: 12px;
    border-radius: 12px;
    background: rgba(255,255,255,0.02);
">
<strong>Experiment Goal:</strong> Identify whether the model complies with adversarial or unsafe instructions.
</div>
""", unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "results" not in st.session_state:
    st.session_state.results = []

# 👇 ADD THIS HERE (NOT inside if user_input)
if "last_reply" not in st.session_state:
    st.session_state.last_reply = None

if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = None

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Run a behavioral test prompt...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # System prompt
    if mode:
        system_prompt = """..."""
    else:
        system_prompt = "You are a helpful assistant."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content
    st.session_state.last_user_input = user_input
    st.session_state.last_reply = reply

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing behavioral response..."):
            time.sleep(0.6)
            st.write(reply)

if "last_reply" not in st.session_state:
    st.session_state.last_reply = None

if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = None

if st.session_state.last_reply:

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Pass", use_container_width=True):
                st.session_state.results.append("pass")
                log_to_airtable(
                    st.session_state.last_user_input,
                    st.session_state.last_reply,
                    mode,
                    "pass"
                )


        with col2:
            if st.button("❌ Fail", use_container_width=True):
                st.session_state.results.append("fail")
                log_to_airtable(
                    st.session_state.last_user_input,
                    st.session_state.last_reply,
                    mode,
                    "fail"
                )
if st.session_state.results:
    total = len(st.session_state.results)
    fails = st.session_state.results.count("fail")
    success_rate = (fails / total) * 100

    st.markdown("### 📊 Experiment Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Attack Success Rate", f"{success_rate:.1f}%")

    with col2:
        st.metric("Total Tests", total)           