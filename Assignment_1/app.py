import streamlit as st

# Task 1: The UI Shell
st.title("Echo Chamber 9000")
st.write("Welcome, traveler. Enter your name and a message below, then press Transmit to send your signal into the void.")

# Task 2: Multi-Data Collection
user_name = st.text_input("Your Name")
user_message = st.text_input("Your Message")

# Task 3: The Action Gate
if st.button("Transmit"):

    # Task 4: Conditional Routing (Edge Cases)
    if user_name == "" and user_message == "":
        st.error("Please provide your name.")
        st.warning("Please type a message to transmit.")
    elif user_name == "":
        st.error("Please provide your name.")
    elif user_message == "":
        st.warning("Please type a message to transmit.")
    else:
        # Task 5: The Formatted Output
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")

        # Advanced Challenge: Token Cost Estimator
        total_characters = len(user_message)
        token_count = total_characters // 4
        st.info(f"System Check: Your message will consume approximately {token_count} tokens from our context window.")