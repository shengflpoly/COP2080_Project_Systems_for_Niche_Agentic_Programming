from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from dotenv import load_dotenv
from Non_LLM_Tool.tool import irrigation_volume
from langchain.agents import create_agent

load_dotenv()

@st.cache_resource
def load_model():
    """Load the Gemini model. Cached so it only loads
    once."""
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return None
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7, # slight creativity for friendly chat
        convert_system_message_to_human=True, # Gemini requires
    )

llm = load_model()

agent = create_agent(

    tools=[irrigation_volume],
    llm=llm

)
