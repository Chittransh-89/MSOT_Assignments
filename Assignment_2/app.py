import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Main Title
st.title("🤖 AI Multiverse Chat")
st.write("Chat with different AI personalities from across the multiverse!")

# Task 1: Sidebar Integration 
st.sidebar.title("App Settings")

#Task 2: Persona Expansion
personality = st.sidebar.selectbox(
    "Choose a Personality",
    [
        "An expert Hacker",
        "A panicked college student at 3 AM",
        "A 1920s Mafia Boss",
        "A highly sarcastic fitness coach",
        "A wise ancient wizard",
        "A hyperactive kindergarten teacher",
        "A gloomy Shakespearean poet"
    ]
)

# Task 3: Parameter Tuning (Slider)
intensity = st.sidebar.slider(
    "Intensity Level",
    min_value=1,
    max_value=10,
    value=5
)

# User Input Field 
user_input = st.text_input("Type your message:")

# Task 5: Dynamic Avatars (Control Flow) 
if personality == "An expert Hacker":
    bot_avatar = "💻"
elif personality == "A panicked college student at 3 AM":
    bot_avatar = "😱"
elif personality == "A 1920s Mafia Boss":
    bot_avatar = "🎩"
elif personality == "A highly sarcastic fitness coach":
    bot_avatar = "💪"
elif personality == "A wise ancient wizard":
    bot_avatar = "🧙"
elif personality == "A hyperactive kindergarten teacher":
    bot_avatar = "🎨"
elif personality == "A gloomy Shakespearean poet":
    bot_avatar = "🎭"
else:
    bot_avatar = "🤖"

# Send Button + Chat Logic
if st.button("SEND"):
    if user_input == "":
        st.warning("Please type a message before sending.")
    else:
        # Prompt Engineering with Intensity
        ai_instructions = f"""
        You are {personality}.
        Respond to the user's message while fully staying in character.
        Your intensity level is {intensity} out of 10.
        - If intensity is 1-3, act very subtly like this personality.
        - If intensity is 4-7, act moderately like this personality.
        - If intensity is 8-10, act EXTREMELY exaggerated and over-the-top.
        
        User's message: {user_input}
        """

        # Generate AI response
        response = model.generate_content(ai_instructions)

        # Task 4: Chat Message UI
        # User's message bubble
        with st.chat_message("user"):
            st.write(user_input)

        # AI's response bubble with dynamic avatar
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(response.text)