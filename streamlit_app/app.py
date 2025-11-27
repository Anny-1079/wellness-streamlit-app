import sys
import os
import uuid
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.langchain_agent import ai_wellness_coach, classify_mood


# 🔗 Define MCP server base URL (your deployed MCP server)
API_URL = "https://mcp-server-s1zh.onrender.com"
MCP_URL = f"{API_URL}/mcp"


def call_mcp_get_wellness_tips(mood: str) -> list[str]:
    """
    Call the MCP tool 'get_wellness_tips' on the remote MCP server
    using JSON-RPC over HTTP.
    """
    request_id = str(uuid.uuid4())

    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "get_wellness_tips",
            "arguments": {"mood": mood},
        },
    }

    # POST to /mcp instead of GET /tips/{mood}
    resp = requests.post(MCP_URL, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # If MCP returned an error
    if "error" in data:
        raise RuntimeError(f"MCP error: {data['error']}")

    result = data.get("result")
    if not result:
        raise RuntimeError("No MCP result returned")

    # --- Parse MCP-style result ---
    # Typical MCP tools/call result shape:
    # {
    #   "jsonrpc": "2.0",
    #   "id": "...",
    #   "result": {
    #       "content": [
    #           { "type": "text", "text": "- tip1\n- tip2\n..." }
    #       ]
    #   }
    # }

    content = result.get("content")
    if isinstance(content, list) and content:
        first = content[0]
        if isinstance(first, dict) and first.get("type") == "text":
            text = first.get("text", "")
            # split back into list items
            lines = [line.strip("- ").strip() for line in text.split("\n") if line.strip()]
            return lines

    # Fallbacks: if server returns direct list or something simpler
    if isinstance(result, list):
        return [str(x) for x in result]

    return [str(result)]


# 🔹 Streamlit UI

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
            # 🧠 Existing AI agent response
            ai_response = ai_wellness_coach(user_input)

            # 🔗 Fetch tips from MCP server via tools/call
            try:
                classified_mood = classify_mood(user_input)
                tips_list = call_mcp_get_wellness_tips(classified_mood)

                tips = "\n".join([f"- {tip}" for tip in tips_list])
                full_response = (
                    f"{ai_response}\n\n"
                    f"**Here are some wellness tips for you (via MCP tool `get_wellness_tips`):**\n{tips}"
                )
            except Exception as e:
                full_response = (
                    f"{ai_response}\n\n"
                    f"(Error calling MCP wellness tool: {e})"
                )

            st.markdown(full_response)

    # Add AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})



# import sys
# import os
# import requests
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agent.langchain_agent import ai_wellness_coach, classify_mood


# # 🔗 Define MCP server API URL
# API_URL = "https://wellness-mcp-server.onrender.com"

# st.title("🧠 AI Daily Wellness Coach (LangChain Agent)")
# st.write("Chat with your AI wellness coach. Share how you're feeling anytime.")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# # Display previous chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Chat input box
# user_input = st.chat_input("How are you feeling today? (e.g. happy, sad, stressed)")

# if user_input:
#     # Display user's message immediately
#     with st.chat_message("user"):
#         st.markdown(user_input)
    
#     # Add user message to session state
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Display AI assistant message container
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             # Existing AI agent response
#             ai_response = ai_wellness_coach(user_input)

#             # 🔗 Fetch tips from MCP server API
#             try:
#                 classified_mood = classify_mood(user_input)
#                 response = requests.get(f"{API_URL}/tips/{classified_mood}")
#                 if response.status_code == 200:
#                     tips_data = response.json()
#                     tips = "\n".join([f"- {tip}" for tip in tips_data["tips"]])
#                     full_response = f"{ai_response}\n\n**Here are some wellness tips for you:**\n{tips}"
#                 else:
#                     full_response = f"{ai_response}\n\n(Sorry, couldn't fetch wellness tips right now.)"
#             except Exception as e:
#                 full_response = f"{ai_response}\n\n(Error fetching tips: {e})"

#             st.markdown(full_response)

#     # Add AI response to session state
#     st.session_state.messages.append({"role": "assistant", "content": full_response})

