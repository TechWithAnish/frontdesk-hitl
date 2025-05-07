from requests import create_help_request
from knowledge import get_knowledge

SALON_INFO = {
    "hours": "9 AM to 6 PM, Monday to Saturday",
    "services": "Haircut, coloring, styling",
    "pricing": "Haircut: $30, Coloring: $50"
}

def handle_call(question, caller_id):
    answer = get_knowledge(question)
    if answer:
        print(f"AI response to {caller_id}: {answer}")
        return answer
    for key, value in SALON_INFO.items():
        if key in question.lower():
            print(f"AI response to {caller_id}: {value}")
            return value
    print(f"AI to {caller_id}: Let me check with my supervisor and get back to you.")
    request_id = create_help_request(question, caller_id)
    return None