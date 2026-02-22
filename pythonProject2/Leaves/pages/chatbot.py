import streamlit as st

st.title("Chatbot")
st.write("This is the chatbot page.")


def chatbot_function() -> str:
    """Return a sample chatbot response."""
    response = "This string contains 'nested quotes' and is properly formatted."
    return response


st.code(chatbot_function())
