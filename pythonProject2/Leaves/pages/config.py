# config.py

import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus

# ------------------ MongoDB Config ------------------

MONGO_USERNAME = "puneethgs113_db_user"
MONGO_PASSWORD = "puneeth@113"  # your real password here
MONGO_CLUSTER = "mitraai.0qzeosr.mongodb.net"
MONGO_DB_NAME = "chatbot_db"

def get_mongo_client():
    try:
        encoded_password = quote_plus(MONGO_PASSWORD)

        uri = f"mongodb+srv://{MONGO_USERNAME}:{encoded_password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"

        client = MongoClient(uri)
        client.admin.command("ping")  # test connection
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

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
