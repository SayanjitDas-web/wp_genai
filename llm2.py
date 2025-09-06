from langchain.prompts import Dict,TypeDiet,Optional
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_AI_API")

llm = GoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = gemini_api_key
)
