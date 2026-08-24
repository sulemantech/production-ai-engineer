from typing import TypedDict
from langgraph.graph import StateGraph, START, END

'''User writes how they feel → LangGraph analyzes the message → identifies the primary feeling → determines intensity → generates an appropriate response.'''

class MoodState(TypedDict):
    message: str
    mood: str
    intensity: str
    response : str

MOODS = ["joy","sadness", "anger", "fear", "calm", "neutral"]
INTENSITY = ["low", "medium", "high"]

'''START
  ↓
analyze_mood
  ↓
analyze_intensity
  ↓
generate_response
  ↓
END'''

graph = StateGraph(MoodState)

def analyse_mood(state:MoodState) ->MoodState:
    message = state["message"]
    if any(word in message for word in [
        "happy",
        "joy",
        "great",
        "amazing",
        "wonderful",
        "excited"
    ]):
        state["mood"] = "joy"
    elif any(word in message for word in ["sad",
        "unhappy",
        "lonely",
        "disappointed",
        "hurt"]):
            state["mood"] = "sadness"
    elif any(word in message for word in ["angry",
        "mad",
        "furious",
        "annoyed",
        "frustrated"]):
            state["mood"] = "anger"
    elif any(word in message for word in [
        "afraid",
        "scared",
        "worried",
        "nervous",
        "anxious"
    ]):
        state["mood"] = "fear"
    elif any(word in message for word in [
        "calm",
        "peaceful",
        "relaxed",
        "comfortable"
    ]):
        state["mood"] = "calm"

    else:
        state["mood"] = "neutral"

    return state

def analyze_intensity(state:MoodState) ->MoodState:
    message = state["message"].lower()
    high_words = [
        "extremely",
        "really",
        "very",
        "completely",
        "absolutely",
        "furious",
        "terrible",
        "awful"
    ]

    low_words = [
        "little",
        "slightly",
        "somewhat",
        "a bit",
        "kind of"
    ]
    if any(word in message for word in high_words):
        state["intensity"] = "high"

    elif any(word in message for word in low_words):
        state["intensity"] = "low"

    else:
        state["intensity"] = "medium"

    return state

def generate_response(state: MoodState) -> MoodState:

    mood = state["mood"]
    intensity = state["intensity"]

    if mood == "joy":

        if intensity == "high":
            response = "That's fantastic! You sound really excited!"

        else:
            response = "It's great to hear that you're feeling good."

    elif mood == "sadness":

        if intensity == "high":
            response = (
                "It sounds like you're having a really difficult time. "
                "Be gentle with yourself today."
            )

        else:
            response = (
                "It sounds like you're having a difficult day. "
                "Take some time for yourself."
            )

    elif mood == "anger":

        response = (
            "It sounds like something has really frustrated you. "
            "Taking a short break might help."
        )

    elif mood == "fear":

        response = (
            "It sounds like you're feeling worried. "
            "Taking things one step at a time may help."
        )

    elif mood == "calm":

        response = (
            "It sounds like you're feeling calm and relaxed. "
            "That's a nice state to be in."
        )

    else:

        response = (
            "Thanks for checking in. "
            "How are you feeling about things today?"
        )

    state["response"] = response

    return state

# Add nodes
graph.add_node("analyse_mood",analyse_mood)
graph.add_node("analyze_intensity",analyze_intensity)
graph.add_node("generate_response",generate_response)

# Add Edges
graph.add_edge(START,"analyse_mood")
graph.add_edge("analyse_mood","analyze_intensity")
graph.add_edge("analyze_intensity", "generate_response")
graph.add_edge("generate_response", END)

app = graph.compile()
result = app.invoke({
    "message": "I'm extremely excited about my new job!",
    "mood": "",
    "intensity": "",
    "response": ""
})

print(result)
