import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# if not TAVILY_API_KEY:
#     raise ValueError("TAVILY_API_KEY is not set in the .env file")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def search_itinerary(
    destination: str,
    duration: str,
    travel_style: str = "",
    budget: str = "",
    interests: str = "",
    starting_point: str = ""
) -> str:
    """
    Research and create travel itinerary information for a destination
    using Tavily web search.

    Args:
        destination: City or country the user wants to visit.
        duration: Trip duration, e.g. '3 days' or '5 days'.
        travel_style: Travel style such as family, solo, luxury,
                      budget, honeymoon, adventure, etc.
        budget: Approximate trip budget.
        interests: User interests such as historical places, nature,
                   shopping, food, museums, nightlife, etc.
        starting_point: Starting location for the trip.

    Returns:
        Web-researched travel information useful for creating an itinerary.
    """

    query = f"""
    Create a practical {duration} travel itinerary for {destination}.
    """

    if starting_point:
        query += f"""
        Traveler is starting from {starting_point}.
        """

    if travel_style:
        query += f"""
        Travel style: {travel_style}.
        """

    if budget:
        query += f"""
        Budget: {budget}.
        """

    if interests:
        query += f"""
        Interests: {interests}.
        """

    query += """
    Research the following:

    1. Top tourist attractions
    2. Best places to visit
    3. Things to do
    4. Recommended restaurants and local food
    5. Approximate travel time between major attractions
    6. Opening hours where available
    7. Entry fees where available
    8. Best time to visit attractions
    9. Local transportation options
    10. Practical travel tips

    Organize the information so another AI agent can use it
    to create a day-by-day itinerary.
    """

    try:

        response = tavily_client.search(
            query=query,
            max_results=3,
            include_answer=True
        )

        results = response.get("results", [])
        answer = response.get("answer", "")

        if not results:
            return (
                f"No itinerary information found for "
                f"{destination}."
            )

        output = []

        output.append(
            f"Travel Research for {destination}\n"
        )

        if answer:
            output.append(
                f"Overall Summary:\n{answer}\n"
            )

        output.append(
            "Detailed Research:\n"
        )

        for index, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "Unknown source"
            )

            url = result.get(
                "url",
                "N/A"
            )

            content = result.get(
                "content",
                "No information available"
            )

            output.append(
                f"""
Source {index}
Title: {title}
URL: {url}
Information:
{content}
"""
            )

        return "\n".join(output)

    except Exception as e:

        return f"Itinerary search failed: {str(e)}"


# if __name__ == "__main__":

#     result = search_itinerary.invoke({
#         "destination": "Kolkata",
#         "duration": "3 days",
#         "travel_style": "budget",
#         "budget": "under 10000 INR",
#         "interests": "historical places, food, culture",
#         "starting_point": "Durgapur"
#     })

#     print(result)