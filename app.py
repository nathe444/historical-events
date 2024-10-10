import streamlit as st
import requests
import dotenv
import os

dotenv.load_dotenv()
hugging_face_api_key = os.getenv("hugging_face_api")

def summarize_with_huggingface(text, api_key, min_length=100, max_length=300):
    """Summarize the provided text using Hugging Face's API."""
    headers = {"Authorization": f"Bearer {hugging_face_api_key}"}
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    
    # Set parameters for summarization
    data = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,  # Minimum length of summary
            "max_length": max_length,  # Maximum length of summary
            "length_penalty": 2.0,     # Length penalty to control length of the output
            "num_beams": 4,            # Number of beams for beam search
            "early_stopping": True      # Stop early if all beams reach EOS token
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        return "Error: Unable to generate summary."

st.set_page_config(page_title="Historical Events Summarizer", page_icon="📜", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    .title {
        font-size: 2.5em;
        color: #ffffff;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    .input-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .input {
        width: 60%;
        padding: 10px;
        border: 1px solid #ffffff;
        border-radius: 5px;
        font-size: 1em;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }
    .button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        font-size: 1em;
        transition: background-color 0.3s;
        margin-left: 10px;
    }
    .button:hover {
        background-color: #2980b9;
    }
    .summary {
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        margin: 20px auto;
        max-width: 80%;
        text-align: justify;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Historical Events Summarizer 📜</div>', unsafe_allow_html=True)

event = st.text_input("Enter a historical event", "", key="event_input", help="Type the historical event you want to summarize here. ",  placeholder="e.g. , The signing of the Declaration of Independence")

if st.button("Summarize", key="summarize_button"):
    if event.strip():  
        summary = summarize_with_huggingface(event, hugging_face_api_key, min_length=100, max_length=500)
        st.markdown(f'<div class="summary">{summary}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a historical event to summarize.")
