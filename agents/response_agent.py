from langchain_mistralai import ChatMistralAI
import os

from dotenv import load_dotenv

from state.tripe_state import TripState


load_dotenv()


api_key = os.getenv("MISTRAL_API_KEY")


llm = ChatMistralAI(
    model_name="mistral-small-2603",
    temperature=0.3,
    api_key=api_key
)


def response_agent(state: TripState):

    # =====================================
    # PostgreSQL MEMORY QUERY
    # =====================================

    if state["memory_query"]:

        memory = state["memory_result"]

        # No data found
        if memory.startswith("NO_STORED_DATA"):

            return {
                "final_response": (
                    "No data stored yet for "
                    f"{state['origin']} to "
                    f"{state['destination']}."
                )
            }

        # Data found
        prompt = f"""
You are the TripMate Memory Agent.

The user is asking about previously
stored travel information.

User question:
{state['user_query']}

Stored PostgreSQL information:
{memory}

Answer the user's question using ONLY
the stored PostgreSQL information.

If the stored information contains
travel tips, show the relevant tips.

Do NOT invent information.

Do NOT use web information.

Keep the answer clear and useful.
"""

        response = llm.invoke(prompt)

        return {
            "final_response": response.content
        }

    # =====================================
    # NORMAL TRIP QUERY
    # =====================================

    prompt = f"""
You are the Final Response Agent of TripMate.

Create a clear and useful final travel plan.

User request:
{state['user_query']}

Destination:
{state['destination']}

Origin:
{state['origin']}

Travel dates:
{state['start_date']}
to
{state['end_date']}

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


Create the final answer.

Use this structure:

1. Trip Summary

2. Flight Options

3. Hotel Options

4. Day-by-Day Itinerary

5. Estimated Budget

6. Travel Tips

Do not invent information.

If information is unavailable, say:

"Information not available."
"""
    if state['origin']==state['destination']:
        return {'final_response':"User pleaes provide different origin and different destination."}
    response = llm.invoke(prompt)

    return {
        "final_response": response.content
    }