import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from openai import OpenAI

st.title("⚙ System Configuration")

# =========================================================
# MongoDB Configuration
# =========================================================

st.subheader("🗄 MongoDB Configuration")

mongo_uri = st.text_input("MongoDB URI", type="password")

if st.button("Connect MongoDB"):

    if not mongo_uri:
        st.warning("Please enter MongoDB URI")
        st.stop()

    try:
        client = MongoClient(
            mongo_uri.strip(),
            serverSelectionTimeoutMS=5000
        )

        # Force connection test
        client.admin.command("ping")

        st.session_state.mongo_client = client
        st.success("✅ MongoDB Connected Successfully")

    except ConfigurationError:
        st.error("❌ Invalid MongoDB URI format")

    except ConnectionFailure:
        st.error("❌ Could not connect to MongoDB server")

    except Exception as e:
        st.error(f"❌ MongoDB Error: {e}")

# =========================================================
# OpenRouter Configuration
# =========================================================

st.divider()
st.subheader("🔑 OpenRouter Configuration")

api_key = st.text_input("OpenRouter API Key", type="password")

if st.button("Connect OpenRouter"):

    if not api_key:
        st.warning("Please enter OpenRouter API key")
        st.stop()

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",  # VERY IMPORTANT
            api_key=api_key.strip()
        )

        # Test connection by fetching models
        models = client.models.list()

        model_list = [model.id for model in models.data]

        if not model_list:
            st.error("No models returned. Check OpenRouter account.")
            st.stop()

        st.session_state.openrouter_api_key = api_key.strip()
        st.session_state.available_models = model_list

        st.success("✅ OpenRouter Connected Successfully")

    except Exception as e:
        st.error(f"❌ OpenRouter Error: {e}")
