# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agent.langchain_agent import ai_wellness_coach

# st.title("🧠 AI Daily Wellness Coach (LangChain Agent)")
# st.write("Chat with your AI wellness coach. Share how you're feeling anytime.")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# # Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Chat input box
# user_input = st.chat_input("How are you feeling today? (e.g. happy, sad, stressed)")

# if user_input:
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             ai_response = ai_wellness_coach(user_input)
#             st.markdown(ai_response)

#     # Add AI response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": ai_response})

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.langchain_agent import ai_wellness_coach

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
            ai_response = ai_wellness_coach(user_input)
            st.markdown(ai_response)

    # Add AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
