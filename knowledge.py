from database import get_db
from datetime import datetime

def add_knowledge(question, answer):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO knowledge_base (question, answer, updated_at) VALUES (?, ?, ?)",
        (question, answer, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_knowledge(question):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT answer FROM knowledge_base WHERE question = ?", (question,))
    result = c.fetchone()
    conn.close()
    return result["answer"] if result else None

def get_all_knowledge():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT question, answer, updated_at FROM knowledge_base")
    results = c.fetchall()
    conn.close()
    return results