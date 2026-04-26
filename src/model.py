from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from dotenv import load_dotenv
from Non_LLM_Tool.tool import irrigation_volume
#from langchain.agents import create_agent
from rag_tool import irrigation_knowledge, irrigation_volume_tool
from langchain.tools import BaseTool
from typing import List
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

#@st.cache_resource
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

tools=[irrigation_volume_tool, irrigation_knowledge]

llm_tools = llm.bind_tools(tools)

def find_tool_by_name(tools: List[BaseTool], tool_name: str) -> BaseTool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")

def run_agent(query: str):
    try:
        messages = [HumanMessage(content=query)]
        while True:
            ai_message = llm_tools.invoke(messages)

            # If the model decides to call tools, execute them and return results
            tool_calls = getattr(ai_message, "tool_calls", None) or []
            if len(tool_calls) > 0:
                messages.append(ai_message)
                for tool_call in tool_calls:
                    # tool_call is typically a dict with keys: id, type, name, args
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    tool_call_id = tool_call.get("id")

                    tool_to_use = find_tool_by_name(tools, tool_name)
                    observation = tool_to_use.invoke(tool_args)
                    #print(f"observation={observation}")

                    messages.append(
                        ToolMessage(content=str(observation), tool_call_id=tool_call_id)
                    )
                # Continue loop to allow the model to use the observations
                continue

            # No tool calls -> final answer
            content = ai_message.content

            if isinstance(content, list):
                content = "".join([c.get("text", "") for c in content])
            return content
            
    except Exception as e:
        return f"Error: {str(e)}"
    
