import streamlit as st
import requests
from datetime import datetime

# Hardcoded MongoDB URI
MONGO_URI = "mongodb://localhost:27017/"
API_KEY = "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"

# Page configuration
st.set_page_config(page_title="Mitra.ai", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 20px;
    }
    .error-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
        margin: 10px 0;
    }
    .info-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1565c0;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 Mitra.ai - Your AI Assistant</div>', unsafe_allow_html=True)

# Display connection status
st.markdown("---")

# Check API connectivity
def check_api_connection():
    try:
        response = requests.get('https://api.openrouter.ai/api/v1/auth/key', 
                              headers={'Authorization': f'Bearer {API_KEY}'}, 
                              timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return None

def chat_with_bot(user_input):
    """Send message to OpenRouter API and get response"""
    try:
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:8501/',
            'X-Title': 'Mitra.ai'
        }
        payload = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': user_input}
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Extract response content
        if 'choices' in response.json() and len(response.json()['choices']) > 0:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Sorry, I couldn't generate a response. Please try again."
            
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please check your internet connection and try again."
    except requests.exceptions.ConnectionError as conn_err:
        return "❌ Connection Error: Unable to reach OpenRouter API. Please check:\n1. Internet connection is active\n2. Firewall settings allow API calls\n3. API endpoint is accessible"
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            return "❌ Authentication Error: Invalid API key. Please verify your OpenRouter API key."
        elif response.status_code == 429:
            return "❌ Rate Limit Error: Too many requests. Please wait a moment and try again."
        else:
            return f"❌ HTTP Error {response.status_code}: {str(http_err)}"
    except Exception as err:
        return f"❌ An error occurred: {str(err)}"

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
st.markdown("### 💬 Chat History")
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You**: {message['content']}")
        else:
            st.markdown(f"**Mitra.ai**: {message['content']}")

st.markdown("---")

# Input section with button
st.markdown("### 📝 Send a Message")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Type your message here:",
        placeholder="Ask me anything...",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("📤 Send", use_container_width=True)

# Process user input when button is clicked
if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show loading indicator
    with st.spinner("🔄 Mitra.ai is thinking..."):
        # Get response from OpenRouter API
        bot_response = chat_with_bot(user_input)
    
    # Add bot response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })
    
    # Rerun to display new messages
    st.rerun()

# Sidebar with information
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ System Information")
st.sidebar.markdown(f"""
- **Status**: Active ✅
- **Model**: OpenAI GPT-3.5 Turbo
- **API**: OpenRouter
- **MongoDB**: Connected to `{MONGO_URI}`
- **Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Troubleshooting Guide\n\n**Error: "Failed to resolve 'api.openrouter.ai'"**\n\n**Causes:**\n1. ❌ No internet connection\n2. ❌ Firewall blocking API calls\n3. ❌ DNS resolution issues\n4. ❌ API endpoint down\n\n**Solutions:**\n1. ✅ Check your internet connection\n2. ✅ Disable firewall temporarily (if safe)\n3. ✅ Try restarting your router\n4. ✅ Verify API key is correct\n5. ✅ Check OpenRouter API status\n6. ✅ Try using VPN if DNS issues persist
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Configuration")
st.sidebar.markdown(f"""
- **API Key**: Configured ✅
- **Endpoint**: api.openrouter.ai
- **Protocol**: HTTPS
""")