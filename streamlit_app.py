import streamlit as st
from claybot import ClayBot
import os
from dotenv import load_dotenv
import random

# Fun loading messages that reflect being part of the team
LOADING_MESSAGES = [
    "Let me check our knowledge base...",
    "Connecting with our platform...",
    "Looking through our features...",
    "Checking our latest updates...",
    "Searching our documentation...",
    "Gathering the best information for you...",
    "Finding the perfect solution...",
    "Consulting our best practices...",
    "Reviewing our platform capabilities...",
    "Crafting the perfect response..."
]

# Try to load API key from environment first
load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

# Page config
st.set_page_config(
    page_title="Claygent",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stChat {
        padding-bottom: 100px;
    }
    .stChatMessage {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #2e2e2e;
    }
    .stChatMessage.assistant {
        background-color: #1e1e1e;
    }
    .css-qri22k {
        background-color: #0e1117;
    }
    .css-1n76uvr {
        width: 100%;
    }
    .welcome-text {
        color: #ffffff;
        font-size: 1.2em;
        margin-bottom: 1em;
    }
    .subheader {
        color: #cccccc;
        font-size: 1em;
        margin-bottom: 2em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    try:
        # Initialize with API key from environment if available
        st.session_state.chatbot = ClayBot(api_key)
    except Exception as e:
        st.error(f"Error initializing: {str(e)}")
        st.stop()

def main():
    st.title("👋 Hi, I'm Claygent!")
    
    # Add a friendly welcome message that emphasizes being part of the team
    st.markdown("""
    <div class="welcome-text">
    I'm part of the Clay team, and I love helping our users succeed with our platform! Whether you want to learn about our features or just chat about how we can help your business grow, I'm here for you.
    </div>
    <div class="subheader">
    Feel free to say hi or ask me anything about our platform and how we can help you achieve your goals.
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How can I help you with Clay today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner(random.choice(LOADING_MESSAGES)):
                try:
                    # Pass st.secrets to the chat method
                    response = st.session_state.chatbot.chat(prompt, st.secrets if not api_key else None)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = "I'm having a bit of trouble accessing our systems. Could you try asking that again?"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()
