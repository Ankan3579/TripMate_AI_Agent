


from dotenv import load_dotenv
from langchain.tools import tool
import os
import requests


# ==============================
# Load environment variables
# ==============================

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


# ==============================
# Country aliases
# ==============================

country_aliases = {
    "india": "IN",
    "bharat": "IN",

    "uk": "GB",
    "united kingdom": "GB",
    "england": "GB",

    "usa": "US",
    "united states": "US",
    "america": "US",

    "uae": "AE",
    "united arab emirates": "AE",
}


# ==============================
# Country → Main Airport
# ==============================

country_main_airport = {
    "IN": "DEL",
    "GB": "LHR",
    "US": "JFK",
    "AE": "DXB",
    "FR": "CDG",
    "DE": "FRA",
    "SG": "SIN",
    "JP": "HND",
    "AU": "SYD",
    "CA": "YYZ",
}


# ==============================
# City → Main Airport
# ==============================

city_main_airport = {
    "kolkata": "CCU",
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "chennai": "MAA",
    "hyderabad": "HYD",
    "pune": "PNQ",

    "london": "LHR",
    "paris": "CDG",
    "dubai": "DXB",
    "singapore": "SIN",
    "tokyo": "HND",
    "new york": "JFK",
    "los angeles": "LAX",
    "frankfurt": "FRA",
    "sydney": "SYD",
}


# ==============================
# Airport Resolver
# ==============================

def resolve_airport(location: str):

    location = location.lower().strip()

    # 1. Check city
    if location in city_main_airport:
        return city_main_airport[location]

    # 2. Check country
    if location in country_aliases:

        country_code = country_aliases[location]

        return country_main_airport.get(country_code)

    # 3. If already an IATA code
    if len(location) == 3:
        return location.upper()

    return None


# ==============================
# Flight Search Tool
# ==============================

@tool
def search_flights(departure: str, arrival: str):
    """
    Search flights between two locations.

    The user can provide city names, country names,
    country aliases, or IATA airport codes.

    Examples:
    Kolkata -> London
    Delhi -> Dubai
    CCU -> LHR
    India -> UK
    """

    # Convert user locations to IATA codes

    departure_iata = resolve_airport(departure)
    arrival_iata = resolve_airport(arrival)

    # Check departure

    if not departure_iata:
        return f"Could not find an airport for departure location: {departure}"

    # Check arrival

    if not arrival_iata:
        return f"Could not find an airport for arrival location: {arrival}"

    # Aviationstack API

    BASE_URL = "https://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "dep_iata": departure_iata,
        "arr_iata": arrival_iata,
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:

        return f"Flight API request failed: {str(e)}"

    # API error

    if "error" in data:
        return data["error"]

    flights = data.get("data", [])

    # No flights

    if not flights:

        return (
            f"No flight data found for "
            f"{departure} ({departure_iata}) → "
            f"{arrival} ({arrival_iata})"
        )

    # Format results

    result = []

    for flight in flights:

     result.append({
    "flight": (flight.get("flight") or {}).get("iata"),

    "airline": (flight.get("airline") or {}).get("name"),

    "flight_date": flight.get("flight_date"),

    "status": flight.get("flight_status"),

    "from": (flight.get("departure") or {}).get("airport"),

    "departure_iata": (flight.get("departure") or {}).get("iata"),

    "departure_delay": (flight.get("departure") or {}).get("delay"),

    "departure_time": (flight.get("departure") or {}).get("scheduled"),

    "to": (flight.get("arrival") or {}).get("airport"),

    "arrival_iata": (flight.get("arrival") or {}).get("iata"),

    "arrival_delay": (flight.get("arrival") or {}).get("delay"),

    "arrival_time": (flight.get("arrival") or {}).get("scheduled"),

    "aircraft": (flight.get("aircraft") or {}).get("registration")
})

    return result


# ==============================
# Test
# ==============================

# if __name__ == "__main__":

#     flight = search_flights.invoke({
#         "departure": "delhi",
#         "arrival": "kolkata"
#     })

#     print(flight)


