import streamlit as st
import requests
import random
from urllib.parse import quote

# PAGE CONFIG
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)

# TITLE
st.title("🎨 AI Image Studio")
st.markdown("Generate stunning AI images using Pollinations AI")

# SIDEBAR SETTINGS
st.sidebar.header("⚙️ Settings")

# Art Style
art_style = st.sidebar.selectbox(
    "🖼️ Art Style",
    [
        "Photorealistic",
        "Digital Art",
        "Oil Painting",
        "Watercolor",
        "Anime",
        "Cyberpunk",
        "Fantasy",
        "Minimalist",
        "Sketch",
        "Impressionist"
    ]
)

# Width & Height Sliders — TASK 1 FIX
width = st.sidebar.slider(
    "📐 Width",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

height = st.sidebar.slider(
    "📏 Height",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

# TASK 3 — Magic Enhance Toggle
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# SURPRISE ME PROMPTS — TASK 4
surprise_prompts = [
    "An astronaut riding a horse on Mars during a thunderstorm",
    "A cyberpunk street food vendor in neon-lit Tokyo at midnight",
    "A dragon made entirely of glowing crystals flying over a medieval city",
    "An underwater city where mermaids use smartphones and drink coffee",
    "A giant robot made of flowers protecting a forest from pollution"
]

# MAIN UI 
st.markdown("### 📝 Enter Your Prompt")

# Prompt Input
user_prompt = st.text_area(
    "Describe the image you want to generate:",
    placeholder="e.g. A beautiful sunset over mountains with golden light...",
    height=100
)

# BUTTONS ROW 
col1, col2 = st.columns([1, 1])

with col1:
    generate_clicked = st.button("🚀 Generate Image", use_container_width=True)

with col2:
    # TASK 4 — Surprise Me Button
    surprise_clicked = st.button("🎲 Surprise Me!", use_container_width=True)

# GENERATION LOGIC 
def generate_image(prompt, art_style, width, height, magic_enhance):
    """Generate image using Pollinations AI"""

    # Build full prompt with art style
    full_prompt = f"{prompt}, {art_style} style"

    # TASK 3 — Magic Enhance
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    # TASK 1 FIX — Width & Height in URL
    encoded_prompt = quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"

    st.info(f"🔄 Generating image... Please wait.")

    try:
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            return response.content, full_prompt
        else:
            st.error(f"❌ Error: {response.status_code}")
            return None, None

    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return None, None

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
        return None, None


# HANDLE GENERATE BUTTON 
if generate_clicked:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt first!")
    else:
        with st.spinner("🎨 Creating your masterpiece..."):
            image_data, full_prompt = generate_image(
                user_prompt,
                art_style,
                width,
                height,
                magic_enhance
            )

        if image_data:
            st.success("✅ Image generated successfully!")

            # Show image
            st.image(image_data, caption=f"🎨 {full_prompt}", use_container_width=True)

            # Show details
            with st.expander("ℹ️ Generation Details"):
                st.write(f"**Style:** {art_style}")
                st.write(f"**Size:** {width} x {height}")
                st.write(f"**Magic Enhance:** {'✅ ON' if magic_enhance else '❌ OFF'}")
                st.write(f"**Full Prompt:** {full_prompt}")

            # TASK 2 FIX — Download button with .png + dynamic filename
            st.download_button(
                label="⬇️ Download Image",
                data=image_data,
                file_name=f"{art_style}_image.png",
                mime="image/png",
                use_container_width=True
            )


# HANDLE SURPRISE ME BUTTON — TASK 4
if surprise_clicked:
    random_prompt = random.choice(surprise_prompts)

    st.markdown(f"### 🎲 Surprise Prompt Selected:")
    st.info(f'"{random_prompt}"')

    with st.spinner("🎨 Generating surprise image..."):
        image_data, full_prompt = generate_image(
            random_prompt,
            art_style,
            width,
            height,
            magic_enhance
        )

    if image_data:
        st.success("✅ Surprise image generated!")

        # Show image
        st.image(image_data, caption=f"🎲 {full_prompt}", use_container_width=True)

        # Show details
        with st.expander("ℹ️ Generation Details"):
            st.write(f"**Surprise Prompt:** {random_prompt}")
            st.write(f"**Style:** {art_style}")
            st.write(f"**Size:** {width} x {height}")
            st.write(f"**Magic Enhance:** {'✅ ON' if magic_enhance else '❌ OFF'}")
            st.write(f"**Full Prompt:** {full_prompt}")

        # TASK 2 FIX — Download with .png
        st.download_button(
            label="⬇️ Download Surprise Image",
            data=image_data,
            file_name=f"{art_style}_surprise_image.png",
            mime="image/png",
            use_container_width=True
        )

# FOOTER
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with ❤️ using Streamlit & Pollinations AI</p>",
    unsafe_allow_html=True
)