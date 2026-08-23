from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



from graph.graph import tripmate_graph


app = FastAPI(
    title="TripMate AI Agent",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this for production
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    user_query: str
    origin: str = ""
    destination: str = ""
    start_date: str = ""
    end_date: str = ""
    budget: str = ""
    travelers: int = 1


@app.get("/")
def root():
    return {
        "message": "TripMate AI Agent is running"
    }


@app.post("/trip")
def trip(request: TripRequest):

    try:

        initial_state = {
            "user_query": request.user_query,
            "origin": request.origin,
            "destination": request.destination,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "budget": request.budget,
            "travelers": request.travelers,

            "flight_result": "",
            "hotel_result": "",
            "itinerary_result": "",
            "memory_result": "",
            "memory_query": True,
            "final_response": ""
        }

        result = tripmate_graph.invoke(initial_state)

        return {
            "success": True,
            "response": result["final_response"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )