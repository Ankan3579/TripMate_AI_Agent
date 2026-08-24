from langchain_mistralai import ChatMistralAI
import os 
from state.tripe_state import TripState
from dotenv import load_dotenv
load_dotenv()
from tools.itenary_tools import search_itinerary
api_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model_name="mistral-small-2603",
    temperature=0,
    api_key=api_key
)


def itinerary_agent(state: TripState):

    itinerary_data = search_itinerary.invoke({
        "destination": state["destination"],
        "duration": "Trip duration based on dates",
        "travel_style": "budget",
        "budget": state["budget"],
        "interests": "",
        "starting_point": state["origin"]
    })

    prompt = f"""
You are the Itinerary Agent of TripMate.

Create a practical travel itinerary.

Origin:
{state['origin']}

Destination:
{state['destination']}

Start date:
{state['start_date']}

End date:
{state['end_date']}

Budget:
{state['budget']}

Travelers:
{state['travelers']}

User query:
{state['user_query']}

Research from Tavily:

{itinerary_data}

Create a day-by-day itinerary.

For each day provide:

Morning:
- Places to visit
- Activities

Afternoon:
- Places to visit
- Activities

Evening:
- Places to visit
- Food or entertainment

Also consider:
- Travel time
- Practical transportation
- Budget
- Opening hours when available

Do not invent information.
"""

    response = llm.invoke(prompt)

    return {
        "itinerary_result": response.content
    }