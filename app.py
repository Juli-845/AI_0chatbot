
import streamlit as st
import os

from dotenv import load_dotenv
from openai import OpenAI

from nlp_utils import preprocess_text
from file_handler import save_chat


# Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")


# Initialize OpenRouter client
client = None

if api_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )


# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}

h1 {
    text-align: center;
    color: #60a5fa;
}

.stChatMessage {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# Application heading
st.title("🤖 AI Chatbot")

st.caption("Powered by Python, NLP and Large Language Models")

st.divider()


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 I am your AI assistant. How can I help you today?"
        }
    ]


# Sidebar
with st.sidebar:

    st.header("Chat Settings")

    st.write("Your personal AI chatbot.")

    if st.button("Clear Conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! 👋 How can I help you?"
            }
        ]
        st.rerun()

    st.divider()

    st.subheader("Technologies")

    st.write("🐍 Python")
    st.write("🧠 NLP")
    st.write("✨ LLM")
    st.write("🌐 Streamlit")

    st.divider()

    st.subheader("Chat Information")

    st.write(
        f"Total messages: {len(st.session_state.messages) - 1}"
    )


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Take user input
user_input = st.chat_input("Ask me anything...")


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # NLP preprocessing
    cleaned_text = preprocess_text(user_input)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                if not client:
                    raise ValueError(
                        "OPENROUTER_API_KEY is missing. "
                        "Please configure your .env file."
                    )

                # Send conversation history to LLM
                response = client.chat.completions.create(

                    # Example free model - verify availability
                    model="google/gemma-4-31b-it:free",

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a friendly and helpful AI assistant. "
                                "Give clear, accurate and easy-to-understand answers."
                            )
                        }
                    ] + [
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                        for message in st.session_state.messages
                    ],

                    max_tokens=1000
                )

                bot_response = (
                    response.choices[0].message.content
                )

                if not bot_response:
                    bot_response = "Sorry, I could not generate a response."

            except Exception as e:

                bot_response = f"Error: {str(e)}"

        st.markdown(bot_response)

    # Save conversation
    save_chat(user_input, bot_response)

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_response
        }
    )

    # Display NLP result
    with st.sidebar.expander("NLP Processing Details"):

        st.write("Original Text:")
        st.write(user_input)

        st.write("Preprocessed Text:")
        st.write(cleaned_text)
