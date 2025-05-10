# Frontdesk Human-in-the-Loop AI Supervisor

A Flask-based system for a salon AI agent that answers caller questions, escalates unknown queries to a supervisor via a web UI, and learns from resolved answers. Built for the Frontdesk Engineering Test.

## Features
- **AI Agent**: Answers known questions (e.g., hours, services) and escalates unknown ones.
- **Supervisor UI**: Displays pending requests, allows resolution, and shows history and learned answers.
- **Database**: Stores help requests and knowledge base using SQLite.
- **Timeout Handling**: Marks unresolved requests as "Unresolved" after 5 minutes.
- **Mocked LiveKit**: Simulates supervisor and caller notifications.
- **Error Handling**: Displays flash messages for invalid inputs and database errors.

## Project Structure
- `agent.py`: AI logic for handling calls.
- `app.py`: Flask app with UI routes.
- `database.py`: SQLite database setup and connection.
- `requests.py`: Manages help requests and timeouts.
- `knowledge.py`: Handles knowledge base updates.
- `templates/`: HTML templates for UI (`index.html`, `history.html`, `learned.html`).
- `frontdesk.db`: SQLite database.
- `requirements.txt`: Python dependencies.

## Setup
1. **Clone Repository**:
   ```bash
   git clone <your-repo-url>
   cd frontdesk-hitl