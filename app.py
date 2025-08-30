import streamlit as st
from llm import genrateWebsite

st.title("Ai website Generator")

prompt = st.chat_input("eneter query...")

if prompt:
    user_message =st.chat_message("user")
    user_message.write(prompt)
    user_message.write("ai is thinking..")
    result = genrateWebsite(prompt)
    if 'htmlvalue' not in st.session_state:
            st.session_state['htmlvalue'] = result
    st.page_link("pages/preview.py",label="preview")