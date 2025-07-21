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
    """
    Classify user input into one of the known mood categories using LLM.
    Maps synonyms to standard keys to ensure API compatibility.
    """
    prompt = f"""
You are a helpful wellness assistant.

Classify the following user input into ONLY ONE of these mood categories:

happy, sad, stressed, angry, anxious, frustrated, confused.

Return ONLY the category word in lowercase.

Examples:
Input: "I feel amazing today!" -> happy
Input: "I'm worried about my exam." -> anxious
Input: "Workload is overwhelming me." -> stressed
Input: "I can't believe he did that!" -> angry
Input: "I'm so confused about this topic." -> confused
Input: "I'm frustrated with my slow progress." -> frustrated

User input: "{user_input}"

Mood category:
"""
    response = llm.invoke(prompt)
    mood = response.content.strip().lower()

    # Map synonyms to known keys
    synonyms = {
        "sadness": "sad",
        "joyful": "happy",
        "good": "happy",
        "excited": "happy",
        "content": "happy",
        "mad": "angry",
        "frustrated": "frustrated",
        "confusion": "confused",
        "confused": "confused",
        "overwhelmed": "stressed",
        "stress": "stressed",
        "anxiety": "anxious",
        "nervous": "anxious",
        "worried": "anxious"
    }

    mood = synonyms.get(mood, mood)

    if mood not in ["happy", "sad", "stressed", "angry", "anxious", "frustrated", "confused"]:
        mood = "neutral"  # default fallback

    return mood


# def classify_mood(user_input: str) -> str:
#     """Use LLM to classify user input into a known mood category."""
#     prompt = f"""
# You are a helpful wellness assistant.

# Classify the following user input into one of these mood categories: happy, sad, stressed, angry, anxious.

# If none of these fit, return the closest category.

# User input: "{user_input}"

# Mood category:
# """
#     response = llm.invoke(prompt)
#     return response.content.strip().lower()

def get_wellness_tips(mood: str) -> str:
    response = requests.get(f"{API_URL}/tips/{mood}")
    if response.status_code == 200:
        data = response.json()
        if data["tips"]:
            return "\n".join(data["tips"])
        else:
            return "No tips available for this mood. Try another mood like happy, sad, stressed, angry, anxious."
    else:
        return "Error fetching wellness tips."


def ai_wellness_coach(user_input: str) -> str:
    mood = classify_mood(user_input)
    tips = get_wellness_tips(mood)

    prompt = f"""
You are a compassionate AI wellness coach.

The user said: "{user_input}"
They are feeling {mood}.

Here are CBT-based wellness tips for them:
{tips}

Combine these tips into a SHORT motivating guidance for the user in a conversational tone, within 5 lines. Avoid long explanations.
"""
    response = llm.invoke(prompt)
    return response.content


    
#     prompt = f"""
# You are a compassionate AI wellness coach.

# The user is feeling {mood}.

# Here are CBT-based wellness tips for them:
# {tips}

# Combine these tips into a motivating, structured guidance for the user in a conversational tone.
# """
    # response = llm.invoke(prompt)
    # return response.content

if __name__ == "__main__":
    user_input = input("How are you feeling today? ")
    print(ai_wellness_coach(user_input))
