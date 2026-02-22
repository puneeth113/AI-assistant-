import streamlit as st
from pymongo import MongoClient
from openai import OpenAI

st.title("⚙ System Configuration")

# ------------------ MongoDB ------------------ #
st.subheader("🗄 MongoDB Configuration")

mongo_uri = st.text_input("MongoDB URI", type="password")

if st.button("Connect MongoDB"):

    if mongo_uri:
        try:
            client = MongoClient(mongo_uri)
            client.admin.command("ping")

            st.session_state.mongo_client = client
            st.success("✅ MongoDB Connected")

        except Exception as e:
            st.error(f"MongoDB Connection Failed: {e}")
    else:
        st.warning("Enter MongoDB URI")

st.divider()

# ------------------ OpenRouter ------------------ #
st.subheader("🔑 OpenRouter Configuration")

api_key = st.text_input("OpenRouter API Key", type="password")

if st.button("Connect OpenRouter"):

    if api_key:

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key.strip()
            )

            models = client.models.list()
            model_list = [m.id for m in models.data]

            st.session_state.openrouter_api_key = api_key.strip()
            st.session_state.available_models = model_list

            st.success("✅ OpenRouter Connected Successfully")

        except Exception as e:
            st.error(f"OpenRouter Connection Failed: {e}")

    else:
        st.warning("Enter OpenRouter API Key")
