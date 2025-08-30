from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_AI_API")

llm = GoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = gemini_api_key
)

html_p = PromptTemplate(
    template="{task} create the website,If the website need to have any images and scripts use external image and script links . Strictly only return the html structure of the website with out having any inline or css in the style tag just return the html structure and not include any markdown like '```' or any other markdown expresions and dont include any comments and statements like explantions any other type of text.",
    input_variables=["task"]
)
css_p = PromptTemplate(
    template="{html} add stylings to the website,If the website need to have any images and fonts use external image and font links . Strictly only return the html with its styling inside the style tag of the website with out having any js scripts in the script tag just return the html + css(in the style tag) and not include any markdown like '```' or any other markdown expresions and dont include any comments and statements like explantions any other type of text.",
    input_variables=["html"]
)
js_p = PromptTemplate(
    template="{html_css} add javascript to html and css of the website,If the website need to have any scripts use external  script links . Strictly only return the html containing style in the style tag and js code i the script tag just return the html structure with the style and js and not include any markdown like '```' or any other markdown expresions and dont include any comments and statements like explantions any other type of text.",
    input_variables=["html_css"]
)

def genrateWebsite(query:str) -> str:
    chain = html_p | llm | css_p | llm | js_p | llm
    result = chain.invoke({"task":query})
    print(result)
    if "```" in result:
        result = result.replace("```","")
        return result
    return result