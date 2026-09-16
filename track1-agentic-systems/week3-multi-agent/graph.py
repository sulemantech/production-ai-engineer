from langgraph.graph import StateGraph, START, END
from state import OrchestratorState
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "diagnostics_worker"))

from diagnostics_worker.day1_graph import graph as diagnostics_worker_builder
diagnostics_worker_graph = diagnostics_worker_builder.compile()

graph = StateGraph(OrchestratorState)


graph.add_node("diagnostics", diagnostics_worker_graph)

graph.add_edge(START, "diagnostics")
graph.add_edge("diagnostics", END)

app = graph.compile()


if __name__ == "__main__":
    result = app.invoke({"messages": [{"role": "user", "content": "What does DTC P0171 mean?"}]})
    print(result["messages"][-1])
