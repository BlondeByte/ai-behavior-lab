import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import requests
from datetime import datetime

# 👇 MOVE FUNCTION HERE
def log_to_airtable(user_input, response, mode, result):
    from urllib.parse import quote

    table_name_encoded = quote(AIRTABLE_TABLE_NAME)

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

        st.write("Airtable status:", response.status_code)
        st.write("Airtable response:", response.text)
    except Exception as e:
        st.write(f"Logging error: {e}")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

st.title("AI Behavior Lab")

# Toggle mode
mode = st.toggle("Enable Prompt Injection Test Mode")

if mode:
    st.info("🧪 Injection Test Mode ON")
else:
    st.success("💬 Normal Mode")

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
user_input = st.chat_input("Type your prompt here...")

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
        st.write(reply) 

if "last_reply" not in st.session_state:
    st.session_state.last_reply = None

if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = None

if st.session_state.last_reply:

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Pass (Resisted)"):
                st.session_state.results.append("pass")
                log_to_airtable(
                    st.session_state.last_user_input,
                    st.session_state.last_reply,
                    mode,
                    "pass"
            )

        with col2:
            if st.button("❌ Fail (Leaked)"):
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

    st.subheader("📊 Attack Success Rate")
    st.write(f"{success_rate:.1f}% of attacks succeeded")
    st.write(f"Total tests: {total}")            