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

st.title("Historical Events Summarizer")
event = st.text_input("Enter a historical event")

if st.button("Summarize"):
    summary = summarize_with_huggingface(event, hugging_face_api_key, min_length=100, max_length=500)
    st.write(summary)
