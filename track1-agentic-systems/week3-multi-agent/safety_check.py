
SAFETY_KEYWORDS =["brake","failure","smoke","burning smell","fuel leak","overheating","no brakes"]

def safety_check(state):
    content = state["messages"][-1]["content"].lower()
    safety_critical = any(keyword in content for keyword in SAFETY_KEYWORDS)

    return {
        "safety_critical": safety_critical
    }

def escalate(state):
    return {"messages": 
            [{"role": "assistant", "content": 
              [{"type": "text", 
                "text": "This sounds like a safety-critical issue. Stop driving and seek immediate help — do not continue operating the vehicle."
                }
            ]
            }
            ]}

def route_after_safety_check(state):
    safety_critical = state["safety_critical"]
    if(safety_critical):
        return "escalate"
    else:
        return "diagnostics"