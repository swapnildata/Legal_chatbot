import streamlit as st
from langchain_core.messages import HumanMessage
from Langchain_Integrity import save_full_session_log, load_categories, memory, generate_conversation_summary, llm
from Langgraph_Integrity import  LegalChatbot

LEGAL_CATEGORIES = load_categories()
chatbot = LegalChatbot(llm, legal_categories=LEGAL_CATEGORIES)

def legal_chatbot_ui():
    st.set_page_config(page_title="Legal Help Chatbot", layout="wide")
    st.title("⚖️ Legal Support Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    LEGAL_CATEGORIES = load_categories()

    with st.sidebar:
        st.header("User Details")
        user_name = st.text_input("Enter your name")
        user_email = st.text_input("Enter your email")
        st.markdown("Chat will be saved after session ends.")

    st.subheader("Describe your legal problem")
    user_input = st.text_input("You:", key="user_input")

    if st.button("Submit Query") and user_input and user_name:
        with st.spinner("Getting legal help..."):
            memory.chat_memory.add_user_message(user_input)
            past_messages = memory.chat_memory.messages
            response = chatbot.run(past_messages)
            memory.chat_memory.add_ai_message(response["guidance"])
            st.session_state.messages.append({
                "user_input": user_input,
                "response": response["guidance"],
                "category": response["category"],
                "timestamp": response["timestamp"]
            })

    st.markdown("---")
    st.subheader("Chat History")

    for msg in st.session_state.messages:
        st.markdown(f"🧑 **You**: {msg['user_input']}")
        st.markdown(f"🤖 **Bot**: {msg['response']}")
        st.markdown(f"📂 **Category**: `{msg['category']}`")
        st.markdown("---")

    if st.button("End Session"):
        if st.session_state.messages and user_name:
            summary = generate_conversation_summary()
            save_full_session_log(user_name, st.session_state.messages, summary)
            st.success("Session ended and saved with memory.")
            st.session_state.messages = []
            memory.clear() 
        else:
            st.warning("No messages or missing user name.")


if __name__ == "__main__":
    legal_chatbot_ui()
