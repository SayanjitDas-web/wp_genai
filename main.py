import streamlit as st
from llm import genrateWebsite

tasks = []

st.title("Ai website generator")
task = st.chat_input("give query to generate website..")

if task:
    human = st.chat_message("user")
    human.write(task)
    with st.spinner("ai is generating...", show_time=True):
        result = genrateWebsite(task)
        if 'htmlvalue' not in st.session_state:
            st.session_state['htmlvalue'] = result
        st.page_link("pages/preview.py",label="preview")
        message = st.chat_message("ai")
        message.code(result)
