import os
from dotenv import load_dotenv
import requests
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

API_URL = "https://wellness-mcp-server.onrender.com"


def classify_mood(user_input: str) -> str:
    """
    Classify user input into one of the known mood categories using LLM.
    If the model cannot determine a mood, return 'unknown'.
    """
    prompt = f"""
You are a wellness assistant that identifies the user's mood based on their message.

Classify the following user input into ONLY ONE of these categories:
happy, sad, stressed, angry, anxious, frustrated, confused.

If the user input does NOT express an emotional state (like greetings, small talk, questions, etc.),
return "unknown" (not neutral).

User input: "{user_input}"

Mood category:
"""
    response = llm.invoke(prompt)
    mood = response.content.strip().lower()

    synonyms = {
        "sadness": "sad",
        "joyful": "happy",
        "good": "happy",
        "excited": "happy",
        "content": "happy",
        "mad": "angry",
        "frustrated": "frustrated",
        "confusion": "confused",
        "overwhelmed": "stressed",
        "stress": "stressed",
        "anxiety": "anxious",
        "nervous": "anxious",
        "worried": "anxious"
    }

    mood = synonyms.get(mood, mood)

    valid_moods = ["happy", "sad", "stressed", "angry", "anxious", "frustrated", "confused"]

    if mood not in valid_moods:
        mood = "unknown"

    return mood


def get_wellness_tips(mood: str) -> str:
    if mood == "unknown":
        return (
            "Hmm, I’m not sure how you’re feeling yet. "
            "Could you share something about your mood so I can help you better?"
        )

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
    mood = classify_mood(user_input).strip().lower()

    # If mood is unknown, handle gracefully
    if mood == "unknown":
        return (
            "I’m not quite sure about your mood yet 🤔. "
            "Could you tell me how you’re feeling — maybe happy, sad, stressed, or something else? "
            "That way I can share some wellness tips with you!"
        )

    tips = get_wellness_tips(mood)

    prompt = f"""
You are a compassionate AI wellness coach.

The user said: "{user_input}"
They are feeling {mood}.

Here are CBT-based wellness tips for them:
{tips}

Combine these tips into a motivating guidance for the user in a warm, conversational tone. 
Make it clear and concise: 

- Start with a short supportive line acknowledging their feeling.
- Briefly explain each tip in one sentence, not just the headline, so they understand how to apply it.
- End with a simple, encouraging closing line.

Keep it informative but not over-explained. Aim for around 5–7 lines total.
"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    user_input = input("How are you feeling today? ")
    print(ai_wellness_coach(user_input))



# import os
# from dotenv import load_dotenv
# import requests
# from langchain_openai import ChatOpenAI

# load_dotenv()

# llm = ChatOpenAI(
#     api_key=os.getenv("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1",
#     # model="llama3-70b-8192",
#     model="llama-3.3-70b-versatile", 
#     temperature=0.3
# )

# API_URL = "https://wellness-mcp-server.onrender.com"


# def classify_mood(user_input: str) -> str:
#     """
#     Classify user input into one of the known mood categories using LLM.
#     Maps synonyms to standard keys to ensure API compatibility.
#     """
#     prompt = f"""
# You are a helpful wellness assistant.

# Classify the following user input into ONLY ONE of these mood categories:

# happy, sad, stressed, angry, anxious, frustrated, confused.

# Return ONLY the category word in lowercase.

# Examples:
# Input: "I feel amazing today!" -> happy
# Input: "I'm worried about my exam." -> anxious
# Input: "Workload is overwhelming me." -> stressed
# Input: "I can't believe he did that!" -> angry
# Input: "I'm so confused about this topic." -> confused
# Input: "I'm frustrated with my slow progress." -> frustrated

# User input: "{user_input}"

# Mood category:
# """
#     response = llm.invoke(prompt)
#     mood = response.content.strip().lower()

#     # Map synonyms to known keys
#     synonyms = {
#         "sadness": "sad",
#         "joyful": "happy",
#         "good": "happy",
#         "excited": "happy",
#         "content": "happy",
#         "mad": "angry",
#         "frustrated": "frustrated",
#         "confusion": "confused",
#         "confused": "confused",
#         "overwhelmed": "stressed",
#         "stress": "stressed",
#         "anxiety": "anxious",
#         "nervous": "anxious",
#         "worried": "anxious"
#     }

#     mood = synonyms.get(mood, mood)

#     if mood not in ["happy", "sad", "stressed", "angry", "anxious", "frustrated", "confused"]:
#         mood = "neutral"  # default fallback

#     return mood


# def get_wellness_tips(mood: str) -> str:
#     response = requests.get(f"{API_URL}/tips/{mood}")
#     if response.status_code == 200:
#         data = response.json()
#         if data["tips"]:
#             return "\n".join(data["tips"])
#         else:
#             return "No tips available for this mood. Try another mood like happy, sad, stressed, angry, anxious."
#     else:
#         return "Error fetching wellness tips."


# def ai_wellness_coach(user_input: str) -> str:
#     mood = classify_mood(user_input).strip().lower()
#     tips = get_wellness_tips(mood)

#     prompt = f"""
# You are a compassionate AI wellness coach.

# The user said: "{user_input}"
# They are feeling {mood}.

# Here are CBT-based wellness tips for them:
# {tips}

# Combine these tips into a motivating guidance for the user in a warm, conversational tone. 
# Make it clear and concise: 

# - Start with a short supportive line acknowledging their feeling.
# - Briefly explain each tip in one sentence, not just the headline, so they understand how to apply it.
# - End with a simple, encouraging closing line.

# Keep it informative but not over-explained. Aim for around 5-7 lines total.
# """

#     response = llm.invoke(prompt)
#     return response.content


# if __name__ == "__main__":
#     user_input = input("How are you feeling today? ")
#     print(ai_wellness_coach(user_input))



