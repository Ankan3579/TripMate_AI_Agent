from langchain_mistralai import ChatMistralAI
import os

from dotenv import load_dotenv
from state.tripe_state import TripState
from tools.postgress_tools import retrieve_trip_memory

load_dotenv()


llm = ChatMistralAI(
    model="mistral-small-2603",
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY")
)


def memory_agent(state: TripState):

    memory = retrieve_trip_memory.invoke({
        "origin": state.get("origin", ""),
        "destination": state.get("destination", ""),
        "last_trip": state.get("last_trip", False)
    })

    # No stored trip
    if memory == "NO_STORED_DATA":

        return {
            "memory_result": "NO_STORED_DATA",
            "final_response": "No stored trip was found."
        }

    prompt = f"""
You are the TripMate Memory Agent.

The user wants information about a previously
stored trip.

User request:
{state["user_query"]}

Stored PostgreSQL information:
{memory}

Answer ONLY using the stored PostgreSQL information.

Do not use web information.

Do not invent information.

Give the stored trip clearly to the user.
"""

    response = llm.invoke(prompt)

    return {
        "memory_result": memory,
        "final_response": response.content
    }