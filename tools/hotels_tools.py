import os
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def search_hotels(
    destination: str,
    check_in: str = "",
    check_out: str = "",
    budget: str = "",
    guests: int = 1
) -> str:
    """
    Search for hotels in a destination using Tavily.

    Args:
        destination: City or location where the user wants to stay.
        check_in: Check-in date in YYYY-MM-DD format.
        check_out: Check-out date in YYYY-MM-DD format.
        budget: User's hotel budget, e.g. "under 3000 INR per night".
        guests: Number of guests.

    Returns:
        Relevant hotel search results from the web.
    """

    query = f"""
    Find hotels in {destination}.
    """

    if check_in and check_out:
        query += f" Check-in: {check_in}, Check-out: {check_out}."

    if budget:
        query += f" Budget: {budget}."

    query += f" Number of guests: {guests}."

    query += """
    Provide useful hotel information including:
    - Hotel name
    - Location
    - Price if available
    - Rating if available
    - Amenities
    - Booking website
    - Distance from major attractions if available
    """

    try:
        response = tavily_client.search(
            query=query,
            max_results=3
        )

        results = response.get("results", [])

        if not results:
            return "No hotels found for the given requirements."

        hotel_results = []

        for result in results:
            hotel_results.append(
                f"""
Hotel Information:
Title: {result.get('title', 'N/A')}
URL: {result.get('url', 'N/A')}
Description: {result.get('content', 'N/A')}
"""
            )

        return "\n".join(hotel_results)

    except Exception as e:
        return f"Hotel search failed: {str(e)}"


# if __name__ == "__main__":

#     result = search_hotels.invoke({
#         "destination": "Kolkata",
#         "check_in": "2026-09-10",
#         "check_out": "2026-09-12",
#         "budget": "under 3000 INR per night",
#         "guests": 2
#     })

#     print(result)