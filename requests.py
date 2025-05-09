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

def resolve_help_request(request_id, answer):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE help_requests SET status = ?, answer = ?, resolved_at = ? WHERE id = ?",
        ("Resolved", answer, datetime.now().isoformat(), request_id)
    )
    c.execute("SELECT question, caller_id FROM help_requests WHERE id = ?", (request_id,))
    request = c.fetchone()
    conn.commit()
    conn.close()
    print(f"Text to caller {request['caller_id']}: Here's the answer: {answer}")
    return request["question"]

def get_pending_requests():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM help_requests WHERE status = ?", ("Pending",))
    results = c.fetchall()
    conn.close()
    return results

def get_request_history():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM help_requests")
    results = c.fetchall()
    conn.close()
    return results