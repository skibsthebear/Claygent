import streamlit as st
from claybot import ClayBot
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Fun loading messages
LOADING_MESSAGES = [
    "Molding your answer...",
    "Spinning the clay wheel...",
    "Shaping the perfect response...",
    "Firing up the knowledge kiln...",
    "Crafting something special...",
    "Turning the gears...",
    "Mining the data clay...",
    "Sculpting your solution...",
    "Polishing the details...",
    "Mixing in some AI magic..."
]

# Check for API key
if not os.getenv("PERPLEXITY_API_KEY"):
    st.error("Error: PERPLEXITY_API_KEY not found in environment variables.")
    st.stop()

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
        st.session_state.chatbot = ClayBot(
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY")
        )
    except Exception as e:
        st.error(f"Error initializing: {str(e)}")
        st.stop()

def main():
    st.title("👋 Hi, I'm Claygent!")
    
    # Add a friendly welcome message
    st.markdown("""
    <div class="welcome-text">
    I'm Clay's other, more friendly AI assistant, ready to help shape your business's future! Whether you want to learn about our platform or just chat, I'm here for you.
    </div>
    <div class="subheader">
    Feel free to say hi or ask me anything about how we can help your business grow.
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Chat with me about Clay or just say hi!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner(random.choice(LOADING_MESSAGES)):
                try:
                    response = st.session_state.chatbot.chat(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = "Oops, looks like I hit a bump in the clay road! Could you try asking that again?"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()
