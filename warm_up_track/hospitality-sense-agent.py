from dotenv import load_dotenv
from typing import TypedDict, List
from langgraph.types import Command, Interrupt
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()

# Initialize Claude Model
llm = ChatAnthropic(
    model="claude-haiku-4-5", 
    temperature=0, 
    max_tokens=1024
)

# State Definition
class HospitalityState(TypedDict):
    review: str
    issues: List[str]
    severity: str
    department: str
    require_human: bool
    human_approved: bool
    notification_sent: bool
    guest_response: str


# Pydantic Schemas for Structured Output
class ExtractionOutput(BaseModel):
    issues: List[str] = Field(description="List of explicit complaints or issues.")
    department: str = Field(description="Department responsible.")

class SeverityOutput(BaseModel):
    severity: str = Field(description="Severity rating: LOW, MEDIUM, or HIGH.")


# Nodes
def analyze_review(state: HospitalityState):
    structured_llm = llm.with_structured_output(ExtractionOutput)
    prompt = f"Analyze the following hotel review and extract key issues:\n\n{state['review']}"
    res: ExtractionOutput = structured_llm.invoke(prompt)

    return {
        "issues": res.issues,
        "department": res.department
    }

def assess_severity(state: HospitalityState):
    structured_llm = llm.with_structured_output(SeverityOutput)
    prompt = f"""
    Based on these issues: {state['issues']} in department: {state['department']},
    determine the severity level (LOW, MEDIUM, HIGH).
    """
    res: SeverityOutput = structured_llm.invoke(prompt)

    return {"severity": res.severity}    

def decide_action(state: HospitalityState):
    is_high_severity = state["severity"].upper() == "HIGH" 
    return {"require_human": is_high_severity}

def route_action(state: HospitalityState):
    if state["require_human"]:
        return "human_review"
    return "auto_action"

def auto_action(state: HospitalityState):
    return {"human_approved": True}

from langgraph.types import interrupt

def human_review(state: HospitalityState):
    decision = interrupt({
        "issues": state["issues"],
        "department": state["department"],
        "severity": state["severity"],
        "question": "Approve handling of this complaint?",
    })
    return {"human_approved": decision}

def notify_owner(state: HospitalityState):
    return {"notification_sent": True}

def guest_response(state: HospitalityState):
    prompt = f"""
    Draft a concise, polite and helpful response to the guest regarding the addressed issues: {state['issues']}.
    Severity: {state['severity']}.
    """
    response = llm.invoke(prompt)
    return {"guest_response": response.content}


# Graph Construction
hospitality_workflow = StateGraph(HospitalityState)

# Add Nodes
hospitality_workflow.add_node("analyze_review", analyze_review)
hospitality_workflow.add_node("assess_severity", assess_severity)
hospitality_workflow.add_node("decide_action", decide_action)
hospitality_workflow.add_node("auto_action", auto_action)
hospitality_workflow.add_node("human_review", human_review)
hospitality_workflow.add_node("notify_owner", notify_owner)
hospitality_workflow.add_node("guest_response", guest_response)

# Connect Edges
hospitality_workflow.add_edge(START, "analyze_review")
hospitality_workflow.add_edge("analyze_review", "assess_severity")
hospitality_workflow.add_edge("assess_severity", "decide_action")

# Conditional Branch
hospitality_workflow.add_conditional_edges(
    "decide_action",
    route_action,
    {
        "auto_action": "auto_action",
        "human_review": "human_review"
    }
)

# Rejoin Branches to Final Steps
hospitality_workflow.add_edge("auto_action", "notify_owner")
hospitality_workflow.add_edge("human_review", "notify_owner")
hospitality_workflow.add_edge("notify_owner", "guest_response")
hospitality_workflow.add_edge("guest_response", END)

# Compile
app = hospitality_workflow.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    initial_state = {
        "review": "Heater is broken and no hot water. I want to meet the management immediately!",
        "issues": [],
        "severity": "",
        "department": "",
        "require_human": False,
        "human_approved": False,
        "notification_sent": False,
        "guest_response": ""
    }

    config = {"configurable": {"thread_id": "review-12345"}}
    # result1 = app.invoke(initial_state, config=config)

    # print("--- Final State After Processing Review ---")
    # print(result1)

    # result2 = app.invoke(Command(resume=False),config=config)
    # print("--- Final State After Resuming ---")
    # print(result2)

    result1 = app.invoke(initial_state, config=config)
    print("--- PAUSED FOR APPROVAL ---")
    print(result1["__interrupt__"])

    answer = input("Approve this? (y/n): ").strip().lower()
    decision = answer == "y"

    result2 = app.invoke(Command(resume=decision), config=config)
    print("--- Resumed ---")
    print(result2)