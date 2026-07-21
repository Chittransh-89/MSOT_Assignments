import streamlit as st
from groq import Groq
import requests
import json
import os
import re
from gtts import gTTS
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="Visual Novel", page_icon="📖", layout="wide")

# load api key from environment
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Please set your GROQ_API_KEY environment variable.")
    st.stop()

# cache groq client so it only creates once
@st.cache_resource
def get_client():
    return Groq(api_key=api_key)

client = get_client()

# sidebar settings
with st.sidebar:
    st.title("Story Settings")
    genre = st.selectbox("Story Genre", ["Fantasy", "Horror", "Sci-Fi", "Mystery", "Romance"])
    art_style = st.selectbox("Art Style", ["anime", "realistic", "watercolor", "comic book", "oil painting"])
    if st.button("Restart Story"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# system prompt that forces groq to always return json
system_prompt = f"""
You are a visual novel narrator for a {genre} story.
Every response must be a valid JSON object with exactly these keys:
{{
  "story_text": "narrative paragraph here",
  "image_prompt": "detailed image prompt with {art_style} art style",
  "options": ["choice 1", "choice 2", "choice 3"]
}}
Never include anything outside the JSON object. No markdown, no extra text, just the JSON.
"""

# initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []

if "options" not in st.session_state:
    st.session_state.options = []

if "started" not in st.session_state:
    st.session_state.started = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📖 AI Visual Novel")

# send message to groq and parse the json back
def get_story(user_input):
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
            temperature=0.9
        )
    except Exception as e:
        st.error(f"API error: {str(e)}")
        return None

    raw = response.choices[0].message.content.strip()

    # save model reply to chat history to keep conversation context
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": raw
    })

    # remove markdown code fences if model added them
    raw = re.sub(r"^```(?:json)?", "", raw).strip()
    raw = re.sub(r"```$", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    st.error("Could not parse AI response.")
    return None

# fetch scene image from pollinations with graceful failure
def get_image(prompt):
    try:
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=800&height=400&nologo=true"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception:
        st.toast("Image server is busy, skipping visual...")
        return None

# convert story text to audio using gtts with graceful failure
def get_audio(text):
    try:
        tts = gTTS(text=text, lang="en")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer
    except Exception:
        st.toast("Audio generation failed, skipping narration...")
        return None

# show start button before the story begins
if not st.session_state.started:
    if st.button("▶ Start Story"):
        with st.spinner("Starting your story..."):
            data = get_story(f"Begin a {genre} visual novel story. Set the scene and give choices.")
            if data:
                image = get_image(data["image_prompt"])
                audio = get_audio(data["story_text"])
                st.session_state.history.append({
                    "story_text": data["story_text"],
                    "image": image,
                    "audio": audio
                })
                st.session_state.options = data["options"]
                st.session_state.started = True
                st.rerun()

# render all story beats stored in session state
for i, beat in enumerate(st.session_state.history):
    st.markdown(f"### Chapter {i + 1}")
    if beat["image"]:
        st.image(beat["image"], use_container_width=True)
    st.write(beat["story_text"])
    if beat["audio"]:
        beat["audio"].seek(0)
        st.audio(beat["audio"], format="audio/mp3")
    st.divider()

# dynamically create one button per choice the ai returned
if st.session_state.started and st.session_state.options:
    st.markdown("**What do you do next?**")
    for i, option in enumerate(st.session_state.options):
        if st.button(option, key=f"option_{len(st.session_state.history)}_{i}"):
            with st.spinner("Continuing your story..."):
                data = get_story(option)
                if data:
                    image = get_image(data["image_prompt"])
                    audio = get_audio(data["story_text"])
                    st.session_state.history.append({
                        "story_text": data["story_text"],
                        "image": image,
                        "audio": audio
                    })
                    st.session_state.options = data["options"]
                    st.rerun()