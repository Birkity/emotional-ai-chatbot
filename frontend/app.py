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
securing_rate = st.sidebar.slider("Securing Rate", 1, 7, 4)

st.sidebar.write("""
**Note:** Adjust these parameters to see how the chatbot's emotional state and responses change. 
High anger might make responses more assertive, while high sadness could lead to more empathetic replies.
""")

# Initialize session state for chat history if not exists
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

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
                "securing_rate": securing_rate,
            },
        ).json()

        # Store and display new message in history
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Bot: {response['response']}")

        # Display chatbot response and emotional states
        st.text_area("Bot:", value=response["response"], height=100)
        st.write(f"Anger Level: {response['anger_level']:.2f}")
        st.write(f"Sadness Level: {response['sadness_level']:.2f}")

# Display chat history
st.subheader("Conversation History")
for message in reversed(st.session_state.chat_history[-20:]):  # Show only last 20 messages
    st.text(message)

st.write("Note: The conversation history shows up to the last 20 messages.")