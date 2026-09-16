from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from typing import Annotated
from operator import add

class OrchestratorState(TypedDict):
    messages: Annotated[list, add]
