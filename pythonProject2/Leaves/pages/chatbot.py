import streamlit as st
import requests

# Hardcoded MongoDB URI
MONGO_URI = "mongodb://localhost:27017/"
API_KEY = "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"

def chat_with_bot(user_input):
    url = 'https://api.openrouter.ai/v1/chat'
    headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
    data = {'input': user_input}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()['output']
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

# Streamlit interface
st.title('Chatbot')

user_input = st.text_input('You:', '')
if user_input:
    response = chat_with_bot(user_input)
    if response:
        st.text(f'Bot: {response}')