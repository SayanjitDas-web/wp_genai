from typing import TypedDict, Optional, List
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize Gemini API
gemini_api_key = os.getenv("GEMINI_AI_API")
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_api_key
)

# Define the state structure
class GraphState(TypedDict):
    destination_type: Optional[str]
    budget: Optional[str]
    interests: List[str]
    final_destination: Optional[str]
    budget_plan: Optional[str]
    recommended_destination: List[str]
    itinerary: Optional[List[str]]

# Node 1: Collect preferences (simulated here)
def collected_preference(state):
    return {
        "destination_type": state.get("destination_type"),
        "budget": state.get("budget"),
        "final_destination": state.get("final_destination"),
        "interests": state.get("interests")
    }

# Node 2: Recommend destinations
def recommended_destination(state):
    prompt = f"""
    The user wants to travel.
    Destination type: {state.get("destination_type")}
    Interests: {state.get("interests")}
    Budget: {state.get("budget")}
    
    Suggest 3 good destinations for this trip. Just list them as bullet points.
    """
    response = llm.invoke(prompt)
    list_res = response.split("\n")
    return {"recommended_destination": list_res}

# Node 3: Budget planning
def budget_planning(state):
    prompt = f"""
    The user selected {state.get("final_destination")}. Their budget is {state.get("budget")}.
    Provide a rough budget breakdown for flights, accommodation, food, activities, and miscellaneous in a valid markdown format.
    """
    response = llm.invoke(prompt)
    return {"budget_plan": response}

# Node 4: Itinerary building
def itinerary_building(state):
    prompt = f"""
    Create a 3-day itinerary for {state.get("final_destination")}.
    The user is interested in {state.get("interests")}.
    Provide it day by day in a valid markdown format.
    """
    response = llm.invoke(prompt)
    list_res = response.split("\n")
    return {"itinerary": list_res}

# Define the workflow graph
workflow = StateGraph(GraphState)
workflow.add_node("collected_preference", collected_preference)
workflow.add_node("recommended_destination", recommended_destination)
workflow.add_node("budget_planning", budget_planning)
workflow.add_node("itinerary_building", itinerary_building)

# Set flow
workflow.set_entry_point("collected_preference")
workflow.add_edge("collected_preference", "recommended_destination")
workflow.add_edge("recommended_destination", "budget_planning")
workflow.add_edge("budget_planning", "itinerary_building")
workflow.add_edge("itinerary_building", END)

# Compile the workflow
ai_travel_planner = workflow.compile()

# Streamlit App
st.title("✈️ AI Travel Planner")

with st.form("travel_form"):
    destination_type = st.selectbox(
        "What kind of destination do you prefer?",
        ["beach", "mountains", "city", "countryside"]
    )
    budget = st.number_input("Enter your budget", min_value=100, step=100, value=1000)
    interests = st.multiselect("Select your interests:", ["food", "nightlife", "nature"])
    final_destination = st.text_input("Enter your preferred destination (optional)")
    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    # Build the input state
    state = GraphState(
        destination_type=destination_type,
        budget=str(budget),
        interests=interests,
        final_destination=final_destination if final_destination else None,
        recommended_destination=[],
        budget_plan=None,
        itinerary=None
    )

    # Run the workflow
    result = ai_travel_planner.invoke(state)

    # Display results (formatted)
    st.subheader("🗺️ Recommended Places")
    recommended_places = result.get("recommended_destination", [])
    if isinstance(recommended_places, list):
        st.markdown("\n".join(recommended_places))
    else:
        st.markdown(recommended_places)

    st.subheader("💰 Budget Plan")
    st.markdown(result.get("budget_plan", "No budget plan available."))

    st.subheader("📅 Itinerary")
    itinerary = result.get("itinerary", [])
    if isinstance(itinerary, list):
        st.markdown("\n".join(itinerary))
    else:
        st.markdown(itinerary)
