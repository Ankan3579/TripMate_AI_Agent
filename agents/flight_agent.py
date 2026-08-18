from langchain_mistralai import ChatMistralAI
import os 
from dotenv import load_dotenv
load_dotenv()
from state.tripe_state import TripState

api_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model="mistral-small-2603",
    temperature=0,
    api_key=api_key
)


def flight_agent(state: TripState):

    prompt = f"""
You are the Flight Agent of TripMate.

User wants to travel from {state['origin']} to {state['destination']}.

Travel details:

Origin:
{state['origin']}

Destination:
{state['destination']}

Start date:
{state['start_date']}

End date:
{state['end_date']}

Number of travelers:
{state['travelers']}

User query:
{state['user_query']}

Find or analyze suitable flight options.

Provide:
- Airline
- Flight information if available
- Departure
- Arrival
- Approximate price if available
- Duration
- Useful travel information

Do not invent flight information.
"""

    response = llm.invoke(prompt)

    return {
        "flight_result": response.content
    }