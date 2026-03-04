import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus


# ------------------ MongoDB Config ------------------

# Always store credentials in Streamlit secrets
MONGO_USERNAME = st.secrets.get("MONGO_USERNAME")
MONGO_PASSWORD = st.secrets.get("MONGO_PASSWORD")
MONGO_CLUSTER = st.secrets.get("MONGO_CLUSTER")
MONGO_DB_NAME = st.secrets.get("MONGO_DB_NAME", "chatbot_db")


def get_mongo_client():
    try:
        # Validate secrets
        if not all([MONGO_USERNAME, MONGO_PASSWORD, MONGO_CLUSTER]):
            st.error("❌ MongoDB credentials are missing in secrets.toml")
            return None

        # Encode password (important if it contains special characters)
        encoded_password = quote_plus(MONGO_PASSWORD)

        # Create MongoDB URI
        uri = (
            f"mongodb+srv://{MONGO_USERNAME}:{encoded_password}"
            f"@{MONGO_CLUSTER}/?retryWrites=true&w=majority"
        )

        # Create client with timeout
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        # Test connection
        client.admin.command("ping")

        return client

    except Exception as e:
        st.error(f"❌ MongoDB Connection Error: {e}")
        return None


def get_database():
    client = get_mongo_client()
    if client:
        return client[MONGO_DB_NAME]
    return None


# ------------------ OpenRouter Config ------------------

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.warning("⚠️ OPENROUTER_API_KEY is missing in secrets.toml")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
