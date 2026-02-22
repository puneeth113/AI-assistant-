import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("Mithra.ai")

# --------- Validate Config --------- #

if "mongo_client" not in st.session_state:
    st.error("⚠ Configure MongoDB first.")
    st.stop()

if "openrouter_api_key" not in st.session_state:
    st.error("⚠ Configure OpenRouter first.")
    st.stop()

if "available_models" not in st.session_state:
    st.error("⚠ OpenRouter models not loaded.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.session_state.openrouter_api_key
)

db = st.session_state.mongo_client["ai_chatbot"]

# --------- Upload Dataset --------- #

st.subheader("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.dataframe(df.head())

    collection_name = st.text_input("Enter Collection Name")

    if st.button("Store Dataset"):

        if collection_name:
            collection = db[collection_name]
            records = df.to_dict(orient="records")
            collection.insert_many(records)

            st.success(f"✅ Stored in collection: {collection_name}")
        else:
            st.warning("Enter collection name")

# --------- Dataset Selection --------- #

st.subheader("📊 Select Dataset")

collections = db.list_collection_names()

if not collections:
    st.info("No datasets available. Upload first.")
    st.stop()

selected_collection = st.selectbox("Choose Dataset", collections)
collection = db[selected_collection]

# --------- Model Selection --------- #

st.subheader("🧠 Select AI Model")

selected_model = st.selectbox(
    "Available Models",
    st.session_state.available_models
)

# --------- Chat Section --------- #

st.subheader("💬 Chat With Your Data")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask about your dataset...")

if user_input:

    # Fetch limited data (avoid token overflow)
    data_sample = list(collection.find({}, {"_id": 0}).limit(50))
    data_text = "\n".join([str(row) for row in data_sample])

    system_prompt = f"""
You are a data assistant.
Answer ONLY using the dataset below.

If answer not found, respond:
"Data not available in uploaded dataset."

Dataset:
{data_text}
"""

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    ai_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    with st.chat_message("assistant"):
        st.write(ai_reply)
