import sqlite3

def init_db():
    conn = sqlite3.connect("frontdesk.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS help_requests (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, caller_id TEXT, status TEXT, created_at TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS knowledge_base (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, updated_at TEXT)")
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("frontdesk.db")
    conn.row_factory = sqlite3.Row
    return conn