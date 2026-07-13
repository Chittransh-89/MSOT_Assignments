import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# API Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Main Title 
st.title("🤖 AI Multiverse Chat")
st.write("Chat with different AI personalities from across the multiverse!")

# Task 1: Initialize the Memory Vault 
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar 
st.sidebar.title("App Settings")

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

intensity = st.sidebar.slider("Intensity Level", 1, 10, 5)

# Clear chat button in sidebar
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Dynamic Avatar Logic
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

# Task 2: Render Chat History
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(message["content"])

# Task 3: Upgrade Input UI (walrus operator)
if user_message := st.chat_input("Say something..."):

    # Task 4a: Save User Message to Memory
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_message)

    # Task 4b: Build AI Prompt with Personality + Intensity
    ai_instructions = f"""
    ACT AS: {personality}
    RULES:
    - You ARE {personality}. Never say you are AI.
    - Intensity = {intensity}/10. 1=subtle, 10=EXTREMELY exaggerated.
    - Use slang and tone of {personality}.
    - Keep under 100 words.
    User message: "{user_message}"
    """

    # Task 4c: Generate AI Response
    response = model.generate_content(ai_instructions)

    # Task 4d: Save AI Response to Memory
    st.session_state.messages.append({"role": "assistant", "content": response.text})

    # Display AI response immediately
    with st.chat_message("assistant", avatar=bot_avatar):
        st.write(response.text)