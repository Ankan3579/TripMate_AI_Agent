from langchain_mistralai import ChatMistralAI
import os 
from dotenv import load_dotenv
load_dotenv()
from state.tripe_state import TripState

from tools.hotels_tools import search_hotels
api_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model_name="mistral-small-2603",
    temperature=0,
    api_key=api_key
)


def hotel_agent(state: TripState):

    hotel_data = search_hotels.invoke({
        "destination": state["destination"],
        "check_in": state["start_date"],
        "check_out": state["end_date"],
        "guests": state["travelers"],
        "budget": state["budget"],
        "preferences": ""
    })

    prompt = f"""
You are the Hotel Agent of TripMate.

The user wants to travel to:

Destination:
{state['destination']}

Check-in:
{state['start_date']}

Check-out:
{state['end_date']}

Travelers:
{state['travelers']}

Budget:
{state['budget']}

Here is the hotel research obtained from Tavily:

{hotel_data}

Analyze the results and provide the most useful hotel options.

Include:
- Hotel name
- Location
- Price if available
- Rating if available
- Amenities
- Booking URL if available

Do not invent information.
"""

    response = llm.invoke(prompt)

    return {
        "hotel_result": response.content
    }