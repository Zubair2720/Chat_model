
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API Key from .env (Local Computer)
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Get API Key from Streamlit Cloud Secrets
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# Page Configuration
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("Powered by Google Gemini API")

# Check API Key
if not API_KEY:
    st.error("GEMINI_API_KEY not found. Please configure API Key.")
    st.stop()

# Gemini Client
@st.cache_resource
def create_client(api_key):
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=60000)
    )

client = create_client(API_KEY)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini Chat
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash-lite"
    )

# Sidebar
with st.sidebar:
    st.header("Settings")

    if st.button("New Chat"):
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(
            model="gemini-3.5-flash-lite"
        )
        st.rerun()

    st.info("Model: Gemini 3.5 Flash Lite")

# Display Previous Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Display User Message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini Response
    with st.chat_message("assistant"):

        with st.spinner("Gemini is thinking..."):

            try:
                response = st.session_state.chat.send_message(
                    message=prompt
                )

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error: {e}")
