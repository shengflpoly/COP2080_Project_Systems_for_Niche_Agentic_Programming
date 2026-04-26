import streamlit as st
from Non_LLM_Tool.tool import crops
from model import run_agent, llm
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
st.title("Farmbot")
st.markdown("", unsafe_allow_html=True)
st.markdown("", unsafe_allow_html=True)
st.divider()


# with st.sidebar:

#     if "crop" not in st.session_state or st.session_state.crop is None:
#         st.session_state.crop = list(crops.keys())[0]

#     st.session_state.crop = st.selectbox(
#         "Select crop",
#         list(crops.keys()),
#         index=list(crops.keys()).index(st.session_state.crop)
#     )

#     st.session_state.crop_coefficient = crops.get(st.session_state.crop, 1.0)

#     st.session_state.area = st.number_input(
#         "Field area (hectares)",
#         min_value=0.0,
#         value=1.0
#     )

#     st.session_state.et0 = st.number_input(
#         "ET₀",
#         min_value=0.0,
#         value=5.0
#     )

#     if st.button("Recalculate"):
#         st.rerun()

# DISPLAY CHAT HISTORY
if not st.session_state.messages:
    # Show welcome message on first load
    with st.chat_message("assistant"):
        st.markdown("Hello, I am your farming chatbot.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# CHAT INPUT
user_input = st.chat_input("Ask about farming stuff.")
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
        with st.spinner("Farmbot is thinking..."):
            try:
                # fix to make the correct function call
                messages_str = "\n".join(f"{m['role']}: {m['content']}"for m in st.session_state.messages)
                response_text = run_agent(messages_str)
                st.session_state.chat_history.append(
                    AIMessage(content=response_text)
                )

            except Exception as e:
                response_text = f"Error calling Gemini API: `{str(e)}`"
    # 3. Show response
    with st.chat_message("assistant"):
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})




