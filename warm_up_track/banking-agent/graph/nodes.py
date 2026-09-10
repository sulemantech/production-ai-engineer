from dotenv import load_dotenv
from langchain_groq import ChatGroq
from investigation.graph import investigation_graph
load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b")


def classify_intent(state):
    customer_message = state["customer_message"]

    prompt = f"""
Classify the customer's request into exactly one of these intents:

- transaction_issue
- account_issue
- general_question
- other

Customer message:
{customer_message}

Return only the intent name.
"""

    response = llm.invoke(prompt)

    return {
        "intent": response.content.strip()
    }



def human_review(state):
    return {
        "response": "The case has been escalated for human review."
    }

def investigation_subgraph(state):
    result = investigation_graph.invoke({"customer_id":state["customer_id"]})
    return {"investigation_result": result}

def route_intent(state):
    intent = state["intent"]

    if intent == "transaction_issue":
        return "investigation"

    return "decide_outcome"

def decide_outcome(state):
    investigation_result = state.get("investigation_result", {})

    if investigation_result.get("refund_eligible"):
        return {"outcome": "refund"}

    if investigation_result.get("duplicate_found"):
        return {"outcome": "clarify"}

    return {"outcome": "human_review"}

def route_outcome(state):
    return state["outcome"]


def refund(state):
    return {
        "response": "Refund processed successfully."
    }


def clarify(state):
    return {
        "response": "More information is needed to investigate this transaction."
    }


def human_review(state):
    return {
        "response": "The case has been escalated for human review."
    }