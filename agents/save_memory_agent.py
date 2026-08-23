from state.tripe_state import TripState
from tools.postgress_tools import save_trip_memory
from dotenv import load_dotenv

load_dotenv()


def save_memory_agent(state: TripState):

    # Don't save memory/retrieval queries
    if state.get("memory_query", False):
        return {}

    print("\n========== SAVE MEMORY ==========")

    print("Origin:", state.get("origin"))
    print("Destination:", state.get("destination"))
    print("Start date:", state.get("start_date"))
    print("End date:", state.get("end_date"))
    print("Budget:", state.get("budget"))
    print("Travelers:", state.get("travelers"))

    save_trip_memory.invoke({
        "origin": state.get("origin"),
        "destination": state.get("destination"),
        "start_date": state.get("start_date"),
        "end_date": state.get("end_date"),
        "budget": state.get("budget"),
        "travelers": state.get("travelers"),
        "user_query": state.get("user_query"),
        "final_response": state.get("final_response")
    })

    print("Trip memory saved!")
    print("================================")

    return {}