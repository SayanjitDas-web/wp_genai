import streamlit as st
from llm import genrateWebsite

st.title("Ai website Generator")

prompt = st.chat_input("eneter query...")

if prompt:
    user_message =st.chat_message("user")
    user_message.write(prompt)