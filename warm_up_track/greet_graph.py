from typing import Dict, TypedDict, Union
from langgraph.graph import StateGraph

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict): # Our state schema
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """Simple node that add greeting message to the state"""
    state["message"] = "AoA " + state["message"] + " how is your day going?"
    return state

graph = StateGraph(AgentState)

graph.add_node("greet", greeting_node)

graph.set_entry_point("greet")
graph.set_finish_point("greet")

app = graph.compile()

result = app.invoke({
    "message":"Suleman"
})

print (result)

