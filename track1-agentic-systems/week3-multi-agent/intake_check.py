import re


def intake_check(state):

    message = state["messages"][-1]["content"].strip()

    # DTC example: P0300, P0420, B1234, C0035, U0100
    dtc_pattern = r"\b[PBCU][0-3][0-9A-F]{3}\b"
    has_dtc = bool(re.search(dtc_pattern, message.upper()))

    # Basic symptom description
    has_symptom = len(message.split()) >= 5

    needs_clarification = not (has_dtc or has_symptom)

    return {
        "needs_clarification": needs_clarification
    }

def ask_clarification(state):
    return {"messages": 
            [{"role": "assistant", 
              "content": [{"type": "text", 
                           "text": "Could you share more detail, a diagnostic code, or a specific symptom description?"}]}]}


def route_after_intake_check(state):

    if state["needs_clarification"]:
        return "clarify"
    else:
        return "diagnostics"