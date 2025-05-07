from database import get_db

conn = get_db()
c = conn.cursor()
c.execute("SELECT * FROM help_requests")
for row in c.fetchall():
    print(dict(row))
c.execute("SELECT * FROM knowledge_base")
for row in c.fetchall():
    print(dict(row))
conn.close()