from langchain_mistralai import ChatMistralAI
import os

from dotenv import load_dotenv
from state.tripe_state import TripState

load_dotenv()


llm = ChatMistralAI(
    model="mistral-small-2603",
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY")
)


def router_agent(state: TripState):

    user_query = state.get("user_query", "")

    prompt = f"""
You are the routing agent of TripMate.

Classify the user's request into exactly ONE category.

USER REQUEST:
{user_query}

Return ONLY one of these words:

MEMORY
NORMAL

Use MEMORY when the user wants information about a
previously stored/saved/past trip.

Examples:

"Please provide my last trip"
MEMORY

"Show my previous trip"
MEMORY

"Give me my Kolkata to London trip"
MEMORY

"Show my saved trip from Kolkata to London"
MEMORY

"What was my last Kolkata to London trip?"
MEMORY

"Show my trip history"
MEMORY


Use NORMAL when the user wants a new travel plan,
new flight search, new hotel search, or new itinerary.

Examples:

"Plan a trip from Kolkata to London"
NORMAL

"Find flights from Kolkata to London"
NORMAL

"Find hotels in London"
NORMAL

"Create a 5 day London itinerary"
NORMAL

Return ONLY:
MEMORY
or
NORMAL
"""

    response = llm.invoke(prompt)

    result = response.content.strip().upper()

    if "MEMORY" in result:
        return {
            "memory_query": True,
            "route": "memory"
        }

    return {
        "memory_query": False,
        "route": "normal"
    }