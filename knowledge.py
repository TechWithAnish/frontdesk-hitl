from database import get_db

# Predefined salon information
SALON_INFO = {
    'hours': "9 AM to 6 PM, Monday to Saturday. Closed Sundays.",
    'services': [
        "Haircuts & Styling",
        "Hair Coloring", 
        "Manicures & Pedicures",
        "Facial Treatments",
        "Eyebrow Shaping",
        "Hair Washing & Conditioning"
    ],
    'pricing': {
        "Haircut": "$45-65",
        "Hair Color": "$80-120", 
        "Manicure": "$25",
        "Pedicure": "$35",
        "Facial": "$60-90",
        "Eyebrow Shaping": "$20"
    },
    'contact': {
        'phone': "(555) 123-4567",
        'email': "hello@beautysalon.com",
        'address': "123 Beauty Street, Salon City, SC 12345"
    }
}

def find_answer(question):
    """Find answer in predefined info or learned knowledge."""
    q = question.lower()
    
    # Check predefined salon info
    if any(word in q for word in ['hour', 'time', 'open', 'close']):
        return SALON_INFO['hours']
    
    if any(word in q for word in ['service', 'what do you do', 'offer']):
        return f"We offer: {', '.join(SALON_INFO['services'])}"
    
    if any(word in q for word in ['price', 'cost', 'how much', 'pricing']):
        pricing_list = [f"{service}: {price}" for service, price in SALON_INFO['pricing'].items()]
        return f"Our pricing: {', '.join(pricing_list)}"
    
    if any(word in q for word in ['contact', 'phone', 'call', 'number']):
        return f"Contact us: Phone: {SALON_INFO['contact']['phone']}, Email: {SALON_INFO['contact']['email']}"
    
    if any(word in q for word in ['address', 'location', 'where']):
        return f"We're located at: {SALON_INFO['contact']['address']}"
    
    # Check learned knowledge base
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT answer FROM knowledge_base WHERE LOWER(question) LIKE ?', 
                   (f'%{q}%',))
    result = cursor.fetchone()
    conn.close()
    
    return result['answer'] if result else None

def add_to_knowledge_base(question, answer):
    """Add new knowledge to the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO knowledge_base (question, answer) VALUES (?, ?)',
                   (question, answer))
    conn.commit()
    conn.close()
    print(f"Added to knowledge base: {question} -> {answer}")

def get_knowledge_base():
    """Get all learned knowledge."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM knowledge_base ORDER BY created_at DESC')
    knowledge = cursor.fetchall()
    conn.close()
    return knowledge