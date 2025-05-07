
import sqlite3
conn = sqlite3.connect("frontdesk.db")
c = conn.cursor()
c.execute("PRAGMA table_info(help_requests)")
print(c.fetchall())
conn.close()