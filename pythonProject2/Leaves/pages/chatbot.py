import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests

# Initialize Flask application
app = Flask(__name__)

# MongoDB URI and OpenRouter API key
MONGO_URI = 'mongodb://localhost:27017/'
API_KEY = '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'

# Initialize MongoDB client and database
client = MongoClient(MONGO_URI)
database = client['your_database_name']
collection = database['your_collection_name']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    response = handle_message(user_message)
    return jsonify({'response': response})

def handle_message(message):
    try:
        # Call to OpenRouter API
        headers = {'Authorization': f'Bearer {API_KEY}'}
        payload = {'input': message}
        response = requests.post('https://api.openrouter.com/v1/chat', json=payload, headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            return response_data.get('answer', 'Sorry, I did not understand that.')[0]
        else:
            return 'Error from OpenRouter API'
    except Exception as e:
        return f'Error occurred: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)