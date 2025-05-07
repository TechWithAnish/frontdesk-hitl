import sqlite3

def migrate_db():
    conn = sqlite3.connect("frontdesk.db")
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE help_requests ADD COLUMN answer TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        c.execute("ALTER TABLE help_requests ADD COLUMN resolved_at TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()