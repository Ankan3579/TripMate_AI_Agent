from langgraph.graph import StateGraph, START, END

from state.tripe_state import TripState

from graph.router import router_agent

from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.itenary_agent import itinerary_agent
from agents.memory_agent import memory_agent
from agents.response_agent import response_agent


# =====================================
# CREATE GRAPH
# =====================================

builder = StateGraph(TripState)


# =====================================
# ADD NODES
# =====================================

builder.add_node(
    "router",
    router_agent
)

builder.add_node(
    "memory_agent",
    memory_agent
)

builder.add_node(
    "flight_agent",
    flight_agent
)

builder.add_node(
    "hotel_agent",
    hotel_agent
)

builder.add_node(
    "itinerary_agent",
    itinerary_agent
)

builder.add_node(
    "response_agent",
    response_agent
)


# =====================================
# START → ROUTER
# =====================================

builder.add_edge(
    START,
    "router"
)


# =====================================
# CONDITIONAL WORKFLOW
# =====================================

builder.add_conditional_edges(
    "router",

    lambda state: state["route"],

    {
        "memory": "memory_agent",
        "normal": "flight_agent"
    }
)


# =====================================
# MEMORY PATH
# =====================================

builder.add_edge(
    "memory_agent",
    END
)


# =====================================
# NORMAL TRIP PATH
# =====================================

builder.add_edge(
    "flight_agent",
    "hotel_agent"
)

builder.add_edge(
    "hotel_agent",
    "itinerary_agent"
)

builder.add_edge(
    "itinerary_agent",
    "response_agent"
)

builder.add_edge(
    "response_agent",
    END
)


# =====================================
# COMPILE
# =====================================

tripmate_graph = builder.compile()