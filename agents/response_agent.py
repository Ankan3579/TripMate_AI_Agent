from langchain_mistralai import ChatMistralAI
import os 
from dotenv import load_dotenv
load_dotenv()
from state.tripe_state import TripState
api_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(
    model="mistral-small-2603",
    temperature=0.3,
    api_key=api_key
)


def response_agent(state: TripState):

    prompt = f"""
You are the Final Response Agent of TripMate.

Create a clear and useful final travel plan for the user.

User request:
{state['user_query']}

Destination:
{state['destination']}

Origin:
{state['origin']}

Travel dates:
{state['start_date']} to {state['end_date']}

Budget:
{state['budget']}

Travelers:
{state['travelers']}


FLIGHT INFORMATION:
{state['flight_result']}


HOTEL INFORMATION:
{state['hotel_result']}


ITINERARY:
{state['itinerary_result']}


Combine all the information into one final travel plan.

Use this structure:

1. Trip Summary

2. Flight Options

3. Hotel Options

4. Day-by-Day Itinerary

5. Estimated Budget

6. Travel Tips

Do not invent information.

If information is unavailable, clearly say:
"Information not available."
"""

    response = llm.invoke(prompt)

    return {
        "final_response": response.content
    }