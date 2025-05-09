
from database import get_db
from datetime import datetime, timedelta

conn = get_db()
c = conn.cursor()
old_time = (datetime.now() - timedelta(minutes=10)).isoformat()
c.execute("UPDATE help_requests SET created_at = ? WHERE id = 10 AND status = ?", (old_time, "Pending"))
conn.commit()
conn.close()