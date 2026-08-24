from langchain_mistralai import ChatMistralAI
import os

from dotenv import load_dotenv
from state.tripe_state import TripState

from tools.flight_tools import search_flights


load_dotenv()

llm = ChatMistralAI(
    model_name="mistral-small-2603",
    temperature=0,
    api_key=os.getenv("MISTRAL_API_KEY")
)


def flight_agent(state: TripState):

    flight_data = search_flights.invoke({
        "departure": state["origin"],
        "arrival": state["destination"]
    })

    prompt = f"""
You are the Flight Agent of TripMate.

User wants to travel from:
{state['origin']}

to:
{state['destination']}

Travel dates:
{state['start_date']} to {state['end_date']}

Travelers:
{state['travelers']}

Actual flight API result:
{flight_data}

Explain the available flight information.

Do not invent flight information.

If the API returned no flight information,
say that flight information is unavailable.
"""

    response = llm.invoke(prompt)

    return {
        "flight_result": response.content
    }