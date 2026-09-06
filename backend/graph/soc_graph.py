from typing import TypedDict

from backend.agents.threat_hunter import threat_hunter
from backend.agents.mitre_agent import map_to_mitre
from backend.agents.explainability_agent import explain_incident
from backend.agents.response_agent import generate_response

from langgraph.graph import StateGraph, START, END


class SOCState(TypedDict, total=False):

    incident: dict

    threat: object

    mitre: dict

    explanation: str

    response: str


def threat_hunter_node(state: SOCState):

    result = threat_hunter(
        state["incident"]
    )

    return {
        "threat": result
    }


def mitre_node(state: SOCState):

    mitre = map_to_mitre(
        state["threat"].attack_type
    )

    return {
        "mitre": mitre
    }


def explainability_node(state: SOCState):

    explanation = explain_incident(
        state["incident"],
        state["threat"],
        state["mitre"]
    )

    return {
        "explanation": explanation
    }


def response_node(state: SOCState):

    response = generate_response(
        state["incident"],
        state["threat"],
        state["mitre"]
    )

    return {
        "response": response
    }


builder = StateGraph(SOCState)

builder.add_node(
    "threat_hunter",
    threat_hunter_node
)

builder.add_node(
    "mitre",
    mitre_node
)

builder.add_node(
    "explainability",
    explainability_node
)

builder.add_node(
    "response",
    response_node
)


builder.add_edge(
    START,
    "threat_hunter"
)

builder.add_edge(
    "threat_hunter",
    "mitre"
)

builder.add_edge(
    "mitre",
    "explainability"
)

builder.add_edge(
    "explainability",
    "response"
)

builder.add_edge(
    "response",
    END
)


soc_graph = builder.compile()
