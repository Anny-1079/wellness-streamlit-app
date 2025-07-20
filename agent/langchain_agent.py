import os
from dotenv import load_dotenv
import requests
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model="llama3-70b-8192",
    temperature=0.3
)

API_URL = "https://wellness-mcp-server.onrender.com"

def classify_mood(user_input: str) -> str:
    """Use LLM to classify user input into a known mood category."""
    prompt = f"""
You are a helpful wellness assistant.

Classify the following user input into one of these mood categories: happy, sad, stressed, angry, anxious.

If none of these fit, return the closest category.

User input: "{user_input}"

Mood category:
"""
    response = llm.invoke(prompt)
    return response.content.strip().lower()

def get_wellness_tips(mood: str) -> str:
    """Fetch CBT-based wellness tips for the user's mood from the MCP server."""
    API_URL = "https://your-mcp-server.onrender.com"
    response = requests.get(f"{API_URL}/tips/{mood}")
    if response.status_code == 200:
        tips = response.json().get("tips", [])
        if tips:
            return "\n".join(tips)
        else:
            return f"No specific tips for {mood}, but remember to take care of yourself today."
    else:
        return "No tips available for this mood."

def ai_wellness_coach(user_input: str) -> str:
    # Step 1. Classify mood
    mood = classify_mood(user_input)
    
    # Step 2. Get tips from MCP server
    tips = get_wellness_tips(mood)
    
    # Step 3. Generate final compassionate response
    prompt = f"""
You are a compassionate AI wellness coach.

The user is feeling {mood}.

Here are CBT-based wellness tips for them:
{tips}

Combine these tips into a motivating, structured guidance for the user in a conversational tone.
"""
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    user_input = input("How are you feeling today? ")
    print(ai_wellness_coach(user_input))
