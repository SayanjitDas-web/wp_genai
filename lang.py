from typing import TypedDict,Optional
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

load_dotenv()

gemini_api_key = os.getenv("GEMINI_AI_API")

llm = GoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = gemini_api_key
)


#statecreate
class graphstate(TypedDict):
    input:Optional[str]=None
    condition:Optional[str]=None
    response:Optional[str]=None
#workflowcreate
workflow=StateGraph(graphstate)
#nodecreate
def greeting_node(state):
    return{"response":"hello,how can I help you?"}
def search_node(state):
    question = state.get("input")
    result= llm.invoke(question)
    return {"response":result}
def classify(question):#classify gretingnode or Question
    con=llm.invoke(f"{question}classify the provided question that is it a valid greeting on a search query and return me the response only in search or greeting ")
def classify_node(state):#condition update greeting or node
    question=state.get("input")
    classification=classify(question)
    return{"codition":classification}
#node add in workflow
workflow.add_node("classify",classify_node)
workflow.add_node("greeting",greeting_node)
workflow.add_node("search",search_node)
def decide_next_node(state):#decision which node select greeting or search that in condition
    return "greeting"if state.get("condition")=="greeting"else"search"
workflow.add_conditional_edges(
    "classify",
    decide_next_node,
    {"greeting":"greeting",
     "search":"search"
     }
     )
workflow.set_entry_point("classify")
workflow.add_edge("greeting",END)
workflow.add_edge("search",END)
app=workflow.compile()
input={"input":"what is ai?"}
result=app.invoke(input)
print(result)