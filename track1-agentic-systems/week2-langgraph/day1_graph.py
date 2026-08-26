from dtc_lookup import search_dtc
from operator import add
from vehicle_issues_lookup import fetch_recalls, fetch_complaints
from vin_decoder import decode_vin_code
from llm_client import call_llm_with_retries
from IPython.display import Image, display



from typing import Annotated
from typing_extensions import TypedDict  # Or 'from typing import TypedDict' in Python 3.12+


from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages  # Changed to plural 'add_messages'


# -----------------------------------------------------------------------------
# Graph Flow
#
#                         ┌──────────────┐
#                         │    START     │
#                         └──────┬───────┘
#                                │
#                                ▼
#                         ┌──────────────┐
#                         │     MODEL    │
#                         │              │
#                         │ Decide what  │
#                         │ to do next   │
#                         └──────┬───────┘
#                                │
#                         should_continue()
#                                │
#                         ┌──────┴──────┐
#                         │             │
#                     "tools"          END
#                         │             │
#                         ▼             ▼
#                  ┌──────────────┐   ┌─────┐
#                  │     TOOLS    │   │ END │
#                  │              │   └─────┘
#                  │ Execute the  │
#                  │ requested    │
#                  │ Python tool  │
#                  └──────┬───────┘
#                         │
#                         │ tool result
#                         │
#                         └──────────────► MODEL
#
# Main agent loop:
#
#              ┌─────────────────────────────┐
#              │                             │
#              ▼                             │
#            MODEL → TOOLS → MODEL → TOOLS ──┘
#              │
#              └──────────────→ END
#
# The model keeps deciding whether it needs another tool.
# Once it no longer requests a tool, the graph ends.
# -----------------------------------------------------------------------------

VEHICLE_TOOLS = [
    {

        "name": "fetch_recalls",
        "description": (
            "Fetch recall information from NHTSA for a vehicle "
            "using its make, model, and model year."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "make": {
                    "type": "string",
                    "description": "Vehicle manufacturer, e.g. Toyota",
                },
                "model": {
                    "type": "string",
                    "description": "Vehicle model, e.g. Corolla",
                },
                "year": {
                    "type": "integer",
                    "description": "Vehicle model year, e.g. 2020",
                },
            },
            "required": ["make", "model", "year"],
        },
    },
    {
        "name": "fetch_complaints",
        "description": (
            "Fetch consumer complaint information from NHTSA for a vehicle "
            "using its make, model, and model year."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "make": {
                    "type": "string",
                    "description": "Vehicle manufacturer, e.g. Toyota",
                },
                "model": {
                    "type": "string",
                    "description": "Vehicle model, e.g. Corolla",
                },
                "year": {
                    "type": "integer",
                    "description": "Vehicle model year, e.g. 2020",
                },
            },
            "required": ["make", "model", "year"],
        },
    },
    {
    "name": "search_dtc",
    "description": (
        "Look up a vehicle diagnostic trouble code (DTC) "
        "and return its details."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "dtc_code": {
                "type": "string",
                "description": (
                    "The diagnostic trouble code to look up, "
                    "for example U0100 or P0171."
                ),
            }
        },
        "required": ["dtc_code"],
    },
},
{
    "name": "decode_vin_code",
    "description": (
        "Decode a VIN code and return vehicle information."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "vin": {
                "type": "string",
                "description": "The VIN code to decode."
            }
        },
        "required": ["vin"]
    }
},


]

# -----------------------------------------------------------------------------
# Tool dispatcher
# -----------------------------------------------------------------------------

TOOL_DISPATCHER = {
    "fetch_recalls": fetch_recalls,
    "fetch_complaints": fetch_complaints,
    "search_dtc": search_dtc,
    "decode_vin_code": decode_vin_code,
}


class AgentState(TypedDict):  # Fixed 'TypeDict' to 'TypedDict'
    messages: Annotated[list, add]


def call_model(state):
    response = call_llm_with_retries(
        state["messages"], 
        tools=VEHICLE_TOOLS
        )
    content = [block.model_dump() for block in response.content]
    message = {"role": "assistant", "content": content}
    return {"messages": [message]}


#----------------------------------------------------------------------
# Router
#----------------------------------------------------------------------

def should_continue(state: AgentState):
    content = state["messages"][-1]["content"]
    if any(block["type"] == "tool_use" for block in content):
        return "tools"
    return END

#---------------------------------------------------------------------
# Tool node
#---------------------------------------------------------------------

def execute_tools(state:AgentState):
    response = state["messages"][-1]["content"]

    tool_results = []

    for block in response:
        if block["type"] != "tool_use":
            continue

        tool_name = block["name"]
        tool_input = block["input"]
        tool_use_id = block["id"]
        print(f"Executing tool: {tool_name}")
        print(f"Input: {tool_input}")
        is_error = False
        tool_function = TOOL_DISPATCHER.get(tool_name, None)
        if tool_function is None:
            result = {
                "error": f"Unknown tool: {tool_name}",
            }
            is_error = True
        else:
            try:
                result = tool_function(**tool_input)
            except Exception as e:
                result = {
                    "error": str(e)
                }
                is_error = True
        tool_results.append(
            {
                "type": "tool_result",
                "is_error": is_error, 
                "tool_use_id": tool_use_id,
                "content": str(result),
            
        })
    return {
        "messages":[
            {
                "role": "user",
                "content": tool_results,
            }
        ]
    }

#----------------------------------------------------------------------
# Build graph
#----------------------------------------------------------------------

graph = StateGraph(AgentState)

graph.add_node(
    "model",
    call_model
)

graph.add_node(
    "tools",
    execute_tools
)

graph.add_edge(START, "model")

graph.add_conditional_edges(
    "model",
    should_continue,
    {
        "tools":"tools",
        END:END,
    }
)

graph.add_edge(
    "tools",
    "model"
)

app = graph.compile()
# display(Image(app.get_graph().draw_mermaid_png("day1_graph")), "")

if __name__ == "__main__":
    result = app.invoke({
        "messages": [{"role": "user", "content": "What does DTC code P0171 mean?"}]
    })
    for msg in result["messages"]:
        print(msg)
    display(Image(app.get_graph().draw_mermaid_png(output_file_path="day1_graph.png")))