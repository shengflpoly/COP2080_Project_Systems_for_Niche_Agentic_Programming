import streamlit as st
from Non_LLM_Tool.tool import crops
from model import agent, llm
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


load_dotenv() # loads environment variables from .env file,including GOOGLE_API_KEY

SYSTEM_PROMPT = """

"""

# PAGE CONFIG
st.set_page_config(
    page_title="",
    page_icon="",
    layout="centered",
)

# INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [] # stores {role,content} dicts for display
if "chat_history" not in st.session_state:
    # LangChain message objects for the LLM
    st.session_state.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]

# HEADER
st.markdown("", unsafe_allow_html=True)
st.markdown("", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.session_state.crop = st.selectbox()
    st.session_state.crop_coefficient = crops[st.session_state.crop]
    st.session_state.area = st.number_input()
    st.session_state.et0 = st.number_input()

    if st.button():
        st.rerun()


# DISPLAY CHAT HISTORY
if not st.session_state.messages:
    # Show welcome message on first load
    with st.chat_message("assistant"):
        st.markdown("Hey there! I'm **Yuki-AI**, your Anime DLC guide! \n\nI can help you find the perfect DLC pack for your SteamDeck. Which anime series are you into?")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# CHAT INPUT
user_input = st.chat_input("Ask about DLC, anime, or SteamDeck games...")
if user_input:
    # 1. user message
    with st.chat_message("user"):
        st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    # 2. Add to LangChain history, call Gemini
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    if llm is None:
        # No API key - show helpful error
        response_text = (
        "**No API key found.**\n\n"
        "Set your Gemini API key before starting:\n"
        "```bash\nexport GOOGLE_API_KEY='your-key-here'\n```\n"
        "Get a free key at [Google AI Studio](https://aistudio.google.com)."
        )
    else:
    # Call the Gemini model
        with st.spinner("Yuki-AI is thinking..."):
            try:
                response = agent.invoke(st.session_state.chat_history)
                response_text = response.content
                # Add AI response to LangChain history for multi-turn memory
                st.session_state.chat_history.append(AIMessage(content=response_text))
            except Exception as e:
                response_text = f"Error calling Gemini API:`{str(e)}`"
    # 3. Show response
    with st.chat_message("assistant"):
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})




