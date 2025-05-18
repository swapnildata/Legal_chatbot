import os
import langchain
import langchain_community
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from datetime import datetime
import yaml
from pathlib import Path
from typing import TypedDict, List
from langchain_core.messages import BaseMessage
import json
from langchain.memory import ConversationBufferMemory
from constants import TEMPERATURE, MODEL,MAX_TOKEN_LIMIT
load_dotenv()
api_key = os.getenv("Gemini_API_key")


llm = ChatGoogleGenerativeAI(model=MODEL, temperature=TEMPERATURE,google_api_key=api_key)
memory = ConversationBufferMemory (llm=llm,memory_key="history",return_messages=True)

def load_categories():
    config_path = Path("config/params.yaml")
    with open(config_path, "r") as f:
        params = yaml.safe_load(f)
    categories_list = []
    for category in params.get("categories", []):
        categories_list.append(category)
    return categories_list


def save_full_session_log(user_name: str, messages: list, summary: str):
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(artifacts_dir, f"{current_date}.json")
    session_entry = {"user_name": user_name,"datetime": str(datetime.now()),"messages": messages, "summary": summary}
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            all_sessions = json.load(file)
    else:
        all_sessions = []
    all_sessions.append(session_entry)
    with open(log_file_path, "w") as file:
        json.dump(all_sessions, file, indent=4)


def generate_conversation_summary():
    full_chat = memory.chat_memory.messages
    conversation_text = ""
    for msg in full_chat:
        role = "User" if msg.type == "human" else "Bot"
        conversation_text += f"{role}: {msg.content}\n"
    prompt = (
        "Summarize the following legal chatbot conversation in 5-7 lines."
        "Highlight the key user concerns, legal categories, and the advice provided.\n\n"
        f"{conversation_text}"
    )
    summary = llm.invoke(prompt)
    return summary.content.strip()

