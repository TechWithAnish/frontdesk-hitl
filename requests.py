from database import get_db
from datetime import datetime, timedelta
import threading
from pytz import timezone

def create_help_request(question, caller_id):
    """Create a new help request and add to knowledge base immediately."""
    ist = timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO help_requests (question, caller_id, status, created_at) 
        VALUES (?, ?, 'pending', ?)
    ''', (question, caller_id, current_time.isoformat()))
    request_id = cursor.lastrowid
    conn.commit()
    
    # Add to knowledge base with "Unresolved" as default
    cursor.execute('INSERT INTO knowledge_base (question, answer, created_at) VALUES (?, ?, ?)',
                   (question, "Unresolved", current_time.isoformat()))
    conn.commit()
    conn.close()
    
    # Mock LiveKit notification
    print(f"[Mock LiveKit] Text to supervisor: Hey, I need help answering '{question}' for caller {caller_id} (Request ID: {request_id}) at {current_time.strftime('%I:%M %p IST')}")
    
    # Start 1-minute timeout timer
    start_timeout_timer(request_id, caller_id, question, current_time)
    
    return request_id

def resolve_request(request_id, answer):
    """Resolve a help request with an answer."""
    ist = timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get request details
    cursor.execute('SELECT * FROM help_requests WHERE id = ? AND status = "pending"', (request_id,))
    request = cursor.fetchone()
    
    if not request:
        conn.close()
        return False
    
    # Update request
    cursor.execute('''
        UPDATE help_requests 
        SET status = 'resolved', answer = ?, resolved_at = ? 
        WHERE id = ?
    ''', (answer, current_time.isoformat(), request_id))
    
    # Update knowledge base with resolved answer
    cursor.execute('''
        UPDATE knowledge_base 
        SET answer = ?, created_at = ? 
        WHERE question = ? AND answer = 'Unresolved'
    ''', (answer, current_time.isoformat(), request['question']))
    
    conn.commit()
    conn.close()
    
    # Mock LiveKit notification to customer
    print(f"[Mock LiveKit] Text to caller {request['caller_id']}: Here's the answer: {answer} at {current_time.strftime('%I:%M %p IST')}")
    
    return True

def start_timeout_timer(request_id, caller_id, question, creation_time):
    """Start 1-minute timeout timer for request."""
    def timeout_handler():
        ist = timezone('Asia/Kolkata')
        current_time = datetime.now(ist)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM help_requests WHERE id = ?', (request_id,))
        result = cursor.fetchone()
        
        if result and result['status'] == 'pending':
            cursor.execute('UPDATE help_requests SET status = "unresolved" WHERE id = ?', (request_id,))
            conn.commit()
            # Mock pop-up notification (simulated via print for now)
            print(f"[ALERT] Notification: Query '{question}' for caller {caller_id} unresolved after 1 minute at {current_time.strftime('%I:%M %p IST')}")
        
        conn.close()
    
    # Set timer for 1 minute (60 seconds)
    timer = threading.Timer(60.0, timeout_handler)
    timer.start()

def get_requests_by_status(status=None):
    """Get requests by status or all requests."""
    ist = timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    conn = get_db()
    cursor = conn.cursor()
    
    if status:
        cursor.execute('SELECT * FROM help_requests WHERE status = ? ORDER BY created_at DESC', (status,))
    else:
        cursor.execute('SELECT * FROM help_requests ORDER BY created_at DESC')
    
    requests = cursor.fetchall()
    conn.close()
    return requests

def check_and_handle_timeouts():
    """Check for and handle timed out requests."""
    ist = timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Find requests older than 1 minute that are still pending
    timeout_threshold = current_time - timedelta(minutes=1)
    cursor.execute('''
        UPDATE help_requests 
        SET status = 'unresolved' 
        WHERE status = 'pending' AND created_at < ?
    ''', (timeout_threshold.isoformat(),))
    
    conn.commit()
    conn.close()