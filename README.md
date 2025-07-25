# Frontdesk Human-in-the-Loop AI Supervisor

A Flask-based system for a salon AI agent that answers caller questions, escalates unknown queries to a human supervisor via a web UI, and learns from resolved answers. This project was developed as part of the Frontdesk Engineering Test to demonstrate skills in system design, modularity, and product UX.

## Overview

This project builds the foundation for an AI receptionist system at Frontdesk, designed to manage customer relationships end-to-end. The AI agent handles incoming calls for a fake salon, answers known questions (e.g., hours, services), and escalates unknown queries to a human supervisor. The supervisor resolves requests via a simple web UI, and the system updates its knowledge base with new answers, ensuring the AI improves over time. Key features include timeout handling, error management, and mocked LiveKit escalations.

## Features
- **AI Agent**: Responds to known questions (e.g., salon hours, services) using predefined data and escalates unknown queries to a supervisor.
- **Supervisor UI**: Allows supervisors to view pending requests, submit answers, see request history (resolved/unresolved), and review learned answers.
- **Database**: Stores help requests and learned answers in SQLite for persistence.
- **Timeout Handling**: Automatically marks unresolved requests as "Unresolved" after 5 minutes with a follow-up notification.
- **Mocked LiveKit**: Simulates supervisor and caller notifications via console logs, fulfilling the requirement to simulate calls/texts.
- **Error Handling**: Displays flash messages (green for success, red for errors) for invalid inputs and database issues.

## Project Structure
- `agent.py`: Contains AI logic to handle calls, respond to known questions, and escalate unknowns.
- `app.py`: Flask application with routes for the UI and call simulation.
- `database.py`: Sets up and manages SQLite database connections and schema.
- `requests.py`: Manages help request lifecycle (create, resolve, timeout) and mocked LiveKit notifications.
- `knowledge.py`: Handles knowledge base updates and retrieval.
- `templates/`:
  - `base.html`: Base template with navigation and styling.
  - `index.html`: Dashboard for simulating calls and resolving pending requests.
  - `history.html`: Displays request history.
  - `learned.html`: Shows learned answers.
- `static/`:
  - `css/style.css`: Stylesheet for UI.
  - `js/main.js`: JavaScript for frontend interactivity.
- `salon.db`: SQLite database file storing help requests and knowledge base.
- `requirements.txt`: Lists Python dependencies (e.g., Flask, Werkzeug, livekit-api).
- `test_timeout.py`, `manual_timeout.py`: Scripts for testing timeout functionality.
- `check_db.py`: Utility to inspect database contents.

## Setup
Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/TechWithAnish/frontdesk-hitl
   cd frontdesk-hitl

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - Ensures Flask (2.3.2) and livekit-api are installed.

4. **Initialize the Database**:
   ```bash
   python -c "from database import init_db; init_db()"
   ```
   - Creates `frontdesk.db` with `help_requests` and `knowledge_base` tables.

5. **Run the Application**:
   ```bash
   python app.py
   ```
   - Starts the Flask server at `http://localhost:5000`.

6. **Access the UI**:
   - Open `http://localhost:5000` in a browser to access the supervisor dashboard.

## Usage
The system supports two main workflows: simulating calls via the AI agent and managing requests via the supervisor UI.

### Simulating Calls
- **Via UI**:
  1. On the dashboard (`http://localhost:5000`), use the "Simulate a Call" form.
  2. Enter a Caller ID (e.g., `caller123`) and a Question (e.g., `What are your hours?`).
  3. Click "Simulate Call".
  4. Check the terminal for console logs (e.g., AI response or escalation).
- **Via Command Line**:
   ```bash
   python -c "from agent import handle_call; handle_call('What are your hours?', 'caller111')"
   ```
   - Expected: `AI response to caller111: 9 AM to 6 PM, Monday to Saturday`.
   ```bash
   python -c "from agent import handle_call; handle_call('What is the parking policy?', 'caller222')"
   ```
   - Expected:
     ```
     AI to caller222: Let me check with my supervisor and get back to you.
     [Mock LiveKit] Text to supervisor: Hey, I need help answering 'What is the parking policy?' for caller caller222 (Request ID: 1)
     ```

### Supervisor UI
- **Dashboard (`http://localhost:5000`)**:
  - Simulate calls and view pending requests.
  - Resolve requests by entering an answer (e.g., “Free parking for clients”) and clicking “Resolve”.
  - Flash messages confirm success (green) or errors (red).
- **History (`http://localhost:5000/history`)**:
  - View all requests (Pending, Resolved, Unresolved) with details like question, answer, and timestamps.
- **Learned Answers (`http://localhost:5000/learned`)**:
  - See the AI’s knowledge base with questions and learned answers.

### Testing Timeout Handling
- Simulate a call:
  ```bash
  python -c "from agent import handle_call; handle_call('What is the refund policy?', 'caller333')"
  ```
- Set the request’s `created_at` to 10 minutes ago:
  ```bash
  python -c "from database import get_db; from datetime import datetime, timedelta; conn = get_db(); c = conn.cursor(); c.execute('UPDATE help_requests SET created_at = ? WHERE id = (SELECT MAX(id) FROM help_requests)', ((datetime.now() - timedelta(minutes=10)).isoformat(),)); conn.commit(); conn.close()"
  ```
- Refresh the dashboard to trigger timeout.
- Expected console log:
  ```
  [Mock LiveKit] Text to caller caller333: Sorry, we couldn't answer 'What is the refund policy?' in time.
  ```

## Design Decisions
- **Database Schema**:
  - `help_requests` table: `id`, `question`, `caller_id`, `status` (Pending/Resolved/Unresolved), `answer`, `created_at`, `resolved_at`.
    - Tracks the lifecycle of requests and links responses to callers.
  - `knowledge_base` table: `question`, `answer`, `updated_at`.
    - Stores learned answers for the AI to reuse.
  - SQLite chosen for simplicity and local development; lightweight for the test’s scope.
- **Timeout Handling**:
  - 5-minute threshold to mark requests as Unresolved.
  - `check_timeouts()` runs on every UI route to ensure timely updates.
  - Follow-up notifications are logged to simulate caller updates.
- **Modularity**:
  - Separated logic into `agent.py` (AI), `requests.py` (help requests), `knowledge.py` (knowledge base), and `database.py` (DB management).
  - Ensures maintainability and scalability.
- **Error Handling**:
  - Try-except blocks for database operations to catch SQLite errors.
  - Flash messages for user feedback (e.g., “Answer is required” for empty inputs).
- **Mocked LiveKit**:
  - Used console logs (`[Mock LiveKit]`) to simulate notifications, avoiding real service integration as per constraints.

## Scaling Considerations
- **Current Capacity**: SQLite handles 10–1,000 requests/day with a single-file DB, suitable for this test.
- **Scaling to 1,000/day**:
  - SQLite can manage this with proper indexing on `help_requests` (e.g., index on `status` and `created_at` for timeout queries).
  - Flask runs on a single-threaded server; for production, use Gunicorn with multiple workers.
- **Future Scaling (10,000+/day)**:
  - Switch to a distributed DB like DynamoDB or PostgreSQL for better concurrency and scalability.
  - Implement a message queue (e.g., Redis, RabbitMQ) for handling escalations and follow-ups asynchronously.
  - Deploy Flask with a load balancer to handle increased traffic.

## Deliverables
- **GitHub Repository**: https://github.com/TechWithAnish/frontdesk-hitl

- **Video Demo**: https://drive.google.com/drive/u/0/folders/1DaeEM3gEe_WjXtTqb6AQOGoNB9qvKJVZ
  - A 5-7 minute screen recording showcasing:
    - Simulating calls via UI and command line.
    - Resolving requests with flash messages.
    - Viewing history and learned answers.
    - Timeout and error handling.
    - Mocked LiveKit logs.

## Learnings
As a fresher, I gained valuable skills through this project:
- **Flask Development**: Learned to build a web app with routes, templates, and flash messages.
- **Database Management**: Understood SQLite schema design, queries, and error handling.
- **Debugging**: Fixed issues like schema mismatches, module imports, and UI rendering.
- **System Design**: Designed a modular system with clear separation of concerns.
- **Time Management**: Balanced speed and structure over 2 months timeline.

## Potential Improvements
- **Real LiveKit Integration**: Implement actual LiveKit calls for Phase 2, enabling live transfers and on-hold functionality.
- **UI Enhancements**: Add filters to the history page (e.g., by status) and improve accessibility (e.g., ARIA labels).
- **Scalability**: Transition to DynamoDB and add a message queue for high-volume requests.
- **Testing**: Add unit tests for `agent.py` and `requests.py` to ensure reliability.

## Notes
- LiveKit integration is mocked via console logs as per project constraints.
- Timeout threshold is set to 5 minutes.
- Tested on Python 3.8+ with Flask 2.3.2 and livekit-api.
