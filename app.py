from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_db
from knowledge import get_knowledge_base
from requests import get_requests_by_status, resolve_request, check_and_handle_timeouts
from agent import handle_call
import os
from flask import render_template, Response

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize database on startup
with app.app_context():
    init_db()

@app.route('/')
def index():
    """Main supervisor dashboard."""
    check_and_handle_timeouts()
    pending_requests = get_requests_by_status('pending')
    return render_template('index.html', requests=pending_requests)

@app.route('/simulate_call', methods=['POST'])
def simulate_call():
    """Simulate a customer call."""
    question = request.form.get('question', '').strip()
    caller_id = request.form.get('caller_id', '').strip()
    
    if not question or not caller_id:
        flash('Both question and caller ID are required!', 'error')
        return redirect(url_for('index'))
    
    try:
        response = handle_call(question, caller_id)
        flash(f'Call simulated successfully! Response: {response}', 'success')
    except Exception as e:
        flash(f'Error simulating call: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/resolve/<int:request_id>', methods=['POST'])
def resolve(request_id):
    """Resolve a help request."""
    answer = request.form.get('answer', '').strip()
    
    if not answer:
        flash('Answer is required!', 'error')
        return redirect(url_for('index'))
    
    success = resolve_request(request_id, answer)
    
    if success:
        flash('Request resolved successfully!', 'success')
    else:
        flash('Failed to resolve request. It may have already been resolved or timed out.', 'error')
    
    return redirect(url_for('index'))

@app.route('/history')
def history():
    """View request history."""
    check_and_handle_timeouts()
    all_requests = get_requests_by_status()
    return render_template('history.html', requests=all_requests)

@app.route('/learned')
def learned():
    """View learned knowledge base."""
    knowledge = get_knowledge_base()
    return render_template('learned.html', knowledge=knowledge)

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard stats."""
    pending = len(get_requests_by_status('pending'))
    resolved = len(get_requests_by_status('resolved'))
    unresolved = len(get_requests_by_status('unresolved'))
    knowledge_count = len(get_knowledge_base())
    
    return jsonify({
        'pending': pending,
        'resolved': resolved,
        'unresolved': unresolved,
        'knowledge_base': knowledge_count
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)