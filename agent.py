from knowledge import find_answer
from requests import create_help_request

def handle_call(question, caller_id):
    """Main function to handle customer calls."""
    print(f"\n📞 Incoming call from {caller_id}: '{question}'")
    
    # Try to find answer
    answer = find_answer(question)
    
    if answer:
        print(f"AI response to {caller_id}: {answer}")
        return answer
    else:
        print(f"AI to {caller_id}: Let me check with my supervisor and get back to you.")
        request_id = create_help_request(question, caller_id)
        return f"Escalated to supervisor (Request ID: {request_id})"

if __name__ == '__main__':
    # Test the agent
    handle_call("What are your hours?", "caller111")
    handle_call("What is the parking policy?", "caller222")