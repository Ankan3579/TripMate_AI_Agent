from typing import TypedDict


class TripState(TypedDict):

    user_query: str

    destination: str
    origin: str

    start_date: str
    end_date: str

    budget: str
    travelers: int

    flight_result: str
    hotel_result: str
    itinerary_result: str

    final_response: str