import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
load_dotenv()
gemini_api_key=os.getenv("GEMINI_AI_API")
llm=GoogleGenerativeAI(model="gemini-2.5-flash",api_key="")
st.title("chatbot")
prompt=st.chat_input("enter any query")
if prompt:
    user_message=st.chat_message("user")
    user_message.write(prompt)
    ai_message = st.chat_message("ai")
    result=llm.invoke(prompt+"return in avalid markdown format")
    if result:
        ai_message.markdown(result)




