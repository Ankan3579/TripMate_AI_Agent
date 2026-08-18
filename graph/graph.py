from langgraph.graph import StateGraph, START, END

from state.tripe_state import TripState

from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.itenary_agent import itinerary_agent
from agents.response_agent import response_agent


graph = StateGraph(TripState)


# Add nodes
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("response_agent", response_agent)


# Flow
graph.add_edge(START, "flight_agent")

graph.add_edge("flight_agent", "hotel_agent")

graph.add_edge("hotel_agent", "itinerary_agent")

graph.add_edge("itinerary_agent", "response_agent")

graph.add_edge("response_agent", END)


tripmate_graph = graph.compile()

if __name__ == "__main__":

    initial_state = {
        "user_query": "Plan a 3 day trip to Kolkata",
        "origin": "Delhi",
        "destination": "Kolkata",
        "start_date": "2026-09-10",
        "end_date": "2026-09-12",
        "budget": "under 15000 INR",
        "travelers": 2,

        "flight_result": "",
        "hotel_result": "",
        "itinerary_result": "",
        "final_response": ""
    }

    result = tripmate_graph.invoke(initial_state)

    print("\n========== FINAL RESPONSE ==========\n")

    print(result["final_response"])