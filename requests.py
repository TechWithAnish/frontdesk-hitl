from database import get_db
from datetime import datetime

def create_help_request(question, caller_id):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO help_requests (question, caller_id, status, created_at) VALUES (?, ?, ?, ?)",
        (question, caller_id, "Pending", datetime.now().isoformat())
    )
    request_id = c.lastrowid
    conn.commit()
    conn.close()
    print(f"Text to supervisor: Hey, I need help answering '{question}' for caller {caller_id}")
    return request_id