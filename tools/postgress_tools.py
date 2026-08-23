from langchain.tools import tool
from sqlalchemy import text

from database.postgress import engine


@tool
def retrieve_trip_memory(
    origin: str = "",
    destination: str = "",
    last_trip: bool = False
):
    """
    Retrieve the latest stored trip for
    an origin and destination.
    """
    if last_trip:

        query = text("""
            SELECT
            id,
            origin,
            destination,
            start_date,
            end_date,
            budget,
            travelers,
            user_query,
            final_response,
            created_at
        FROM trip_memory
        ORDER BY created_at DESC
        LIMIT 1
    """)

    else:

        query = text("""
        SELECT
            id,
            origin,
            destination,
            start_date,
            end_date,
            budget,
            travelers,
            user_query,
            final_response,
            created_at
        FROM trip_memory
        WHERE LOWER(origin) = LOWER(:origin)
        AND LOWER(destination) = LOWER(:destination)
        ORDER BY created_at DESC
        LIMIT 1
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "origin": origin,
                "destination": destination
            }
        ).mappings().first()

    if not result:

        return (
            "NO_STORED_DATA: "
            f"No stored data found for "
            f"{origin} to {destination}."
        )

    return f"""
STORED TRIP DATA

Origin:
{result["origin"]}

Destination:
{result["destination"]}

Start date:
{result["start_date"]}

End date:
{result["end_date"]}

Budget:
{result["budget"]}

Travelers:
{result["travelers"]}

Previous user query:
{result["user_query"]}

Previous TripMate response:
{result["final_response"]}

Created:
{result["created_at"]}
"""


@tool
def save_trip_memory(
    origin: str,
    destination: str,
    start_date: str,
    end_date: str,
    budget: str,
    travelers: int,
    user_query: str,
    final_response: str
) -> str:
    """
    Save a completed TripMate trip
    into PostgreSQL.
    """

    query = text("""
        INSERT INTO trip_memory
        (
            origin,
            destination,
            start_date,
            end_date,
            budget,
            travelers,
            user_query,
            final_response
        )
        VALUES
        (
            :origin,
            :destination,
            :start_date,
            :end_date,
            :budget,
            :travelers,
            :user_query,
            :final_response
        )
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "origin": origin,
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "budget": budget,
                "travelers": travelers,
                "user_query": user_query,
                "final_response": final_response
            }
        )

    return "Trip saved successfully."

@tool
def retrieve_latest_trip():
    """
    Retrieve the user's most recently stored trip.
    """

    query = text("""
        SELECT
            id,
            origin,
            destination,
            start_date,
            end_date,
            budget,
            travelers,
            user_query,
            final_response,
            created_at
        FROM trip_memory
        ORDER BY created_at DESC
        LIMIT 1
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        row = result.mappings().first()

    if row:
        return dict(row)

    return "No previous trip found."