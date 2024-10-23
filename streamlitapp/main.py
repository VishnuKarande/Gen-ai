import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-70b-8192'

# Store conversation history
conversation = [
    {
        "role": "system",
        "content": "You are a chat bot designed only to answer questions about footballer Christiano Ronaldo. You do not know anything else. If someone asks questions on topics apart from Christiano Ronaldo, just say you don't know."
    }
]

def get_groq_response(question):
    global conversation
    messages = conversation + [
        {
            "role": "user",
            "content": question,
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096
    )

    conversation.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })

    return response.choices[0].message.content

# Streamlit app title
st.title("Christiano Ronaldo Chatbot")

# Display an image placeholder
st.image(r"E:\Gen-ai\streamlitapp\GOAL.png", width=700, caption="Christiano Ronaldo")

# Adjust CSS for padding and text wrapping
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;  /* Adjust this value as needed */
    padding-bottom: 1rem; /* Ensure bottom content is visible */
    padding-left: 1rem;
    padding-right: 1rem;
}
.css-1r6slb0 {
    white-space: normal !important;
}
.sidebar-text {
    white-space: normal !important;
    word-wrap: break-word;
}
</style>
""", unsafe_allow_html=True)

# Chat interface
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

def send_message():
    question = input_box
    if question:
        st.session_state.conversation.append({"role": "user", "content": question})
        response = get_groq_response(question)
        st.session_state.conversation.append({"role": "assistant", "content": response})

# Input box for user query
input_box = st.text_input("Enter your query about Christiano Ronaldo:")

# Button to get response
if st.button("Send"):
    send_message()

# Display conversation
user_profile_pic = "E:\Gen-ai\streamlitapp\man-avatar-icon-flat-vector.jpg"
assistant_profile_pic = "E:\Gen-ai\streamlitapp\ChatGPT-Logo.png"
for message in st.session_state.conversation:
    if message["role"] == "system":
        st.image(assistant_profile_pic, width=30, output_format='PNG')
        st.markdown(f"**System:** {message['content']}")
    elif message["role"] == "user":
        st.image(user_profile_pic, width=30, output_format='PNG')
        st.markdown(f"**You:** {message['content']}")
    else:
        st.image(assistant_profile_pic, width=30, output_format='PNG')
        st.markdown(f"**Assistant:** {message['content']}")

# Additional Streamlit widgets for beautification
st.sidebar.header("my App")
st.sidebar.markdown('<div class="sidebar-text">This app allows you to ask questions about the legendary footballer Christiano Ronaldo. Feel free to explore and learn more about his career and achievements!</div>', unsafe_allow_html=True)

# Add a footer
st.markdown("---")
st.markdown("Made by Vishnu")