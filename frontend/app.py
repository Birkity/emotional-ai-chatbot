import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://127.0.0.1:5000"

# Streamlit App Title
st.title("Emotional AI Chatbot Using Dorner's Psi Theory")

# Sidebar for Psi Theory Parameters
st.sidebar.header("Adjust Psi Theory Parameters (Scale: 1-7)")
valence = st.sidebar.slider("Valence Level", 1, 7, 4)
arousal = st.sidebar.slider("Arousal Level", 1, 7, 4)
selection_threshold = st.sidebar.slider("Selection Threshold", 1, 7, 4)
resolution_level = st.sidebar.slider("Resolution Level", 1, 7, 4)
goal_directedness = st.sidebar.slider("Goal-Directedness", 1, 7, 4)
securing_rate = st.sidebar.slider("Securing Rate", 1, 7, 4)  # Note: securing_rate isn't used in calculation but is included for completeness

# Chat Interface
st.header("Chat with the Emotional AI Bot")
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        # Send user input and parameters to the backend
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "input": user_input,
                "valence": valence,
                "arousal": arousal,
                "selection_threshold": selection_threshold,
                "resolution_level": resolution_level,
                "goal_directedness": goal_directedness,
            },
        ).json()

        # Display chatbot response and emotional states
        st.text_area("Bot:", value=response["response"], height=100)
        st.write(f"Anger Level: {response['anger_level']:.2f}")
        st.write(f"Sadness Level: {response['sadness_level']:.2f}")