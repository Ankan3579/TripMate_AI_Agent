from typing import TypedDict


class TripState(TypedDict, total=False):

    # User request
    user_query: str

    # Trip details
    origin: str
    destination: str

    start_date: str
    end_date: str

    budget: float
    travelers: int

    # Router
    route: str
    memory_query: bool

    # PostgreSQL memory
    memory_result: str

    # Agent results
    flight_result: str
    hotel_result: str
    itinerary_result: str

    # Final answer
    final_response: str