import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://127.0.0.1:5000"

# Streamlit App Title with Custom Styling
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .stButton button {
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 10px;
    }
    .stTextArea textarea {
        border-radius: 5px;
        padding: 10px;
    }
    .chat-history {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    .emotion-levels {
        background-color: #e6f3ff;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">Emotional AI Chatbot Using Dorner\'s Psi Theory</div>', unsafe_allow_html=True)

# Sidebar for Psi Theory Parameters
st.sidebar.header("Adjust Psi Theory Parameters (Scale: 1-7)")
valence = st.sidebar.slider("Valence Level", 1, 7, 4)
arousal = st.sidebar.slider("Arousal Level", 1, 7, 4)
selection_threshold = st.sidebar.slider("Selection Threshold", 1, 7, 4)
resolution_level = st.sidebar.slider("Resolution Level", 1, 7, 4)
goal_directedness = st.sidebar.slider("Goal-Directedness", 1, 7, 4)
securing_rate = st.sidebar.slider("Securing Rate", 1, 7, 4)

st.sidebar.markdown(
    """
    **Note:** Adjust these parameters to see how the chatbot's emotional state and responses change. 
    - High anger might make responses more assertive.
    - High sadness could lead to more empathetic replies.
    """
)

# Initialize session state for chat history if not exists
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat Interface
st.header("Chat with the Emotional AI Bot")

# Input and Send Button in Columns
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("You: ", "", placeholder="Type your message here...")
with col2:
    if st.button("Send", key="send_button"):
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
if user_input:
    st.markdown('<div class="emotion-levels">', unsafe_allow_html=True)
    st.write(f"**Anger Level:** {response['anger_level']:.2f}")
    st.write(f"**Sadness Level:** {response['sadness_level']:.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

# Display chat history
st.subheader("Conversation History")
st.markdown('<div class="chat-history">', unsafe_allow_html=True)
for message in reversed(st.session_state.chat_history[-20:]):  # Show only last 20 messages
    if message.startswith("You:"):
        st.markdown(f"<p style='color: #4A90E2;'>{message}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: #333333;'>{message}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.write("Note: The conversation history shows up to the last 20 messages.")