from database import get_db

def get_knowledge(question):
         conn = get_db()
         c = conn.cursor()
         c.execute("SELECT answer FROM knowledge_base WHERE question = ?", (question,))
         result = c.fetchone()
         conn.close()
         return result["answer"] if result else None