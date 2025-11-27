import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.langchain_agent import ai_wellness_coach, classify_mood


# 🔗 Define MCP server API URL
API_URL = "https://wellness-mcp-server.onrender.com"

st.title("🧠 AI Daily Wellness Coach (LangChain Agent)")
st.write("Chat with your AI wellness coach. Share how you're feeling anytime.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
user_input = st.chat_input("How are you feeling today? (e.g. happy, sad, stressed)")

if user_input:
    # Display user's message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display AI assistant message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Existing AI agent response
            ai_response = ai_wellness_coach(user_input)

            # 🔗 Fetch tips from MCP server API
            try:
                classified_mood = classify_mood(user_input)
                response = requests.get(f"{API_URL}/tips/{classified_mood}")
                if response.status_code == 200:
                    tips_data = response.json()
                    tips = "\n".join([f"- {tip}" for tip in tips_data["tips"]])
                    full_response = f"{ai_response}\n\n**Here are some wellness tips for you:**\n{tips}"
                else:
                    full_response = f"{ai_response}\n\n(Sorry, couldn't fetch wellness tips right now.)"
            except Exception as e:
                full_response = f"{ai_response}\n\n(Error fetching tips: {e})"

            st.markdown(full_response)

    # Add AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})


