from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db
from requests import get_pending_requests, resolve_help_request, get_request_history, check_timeouts
from knowledge import get_all_knowledge, add_knowledge
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages

@app.route("/")
def index():
    try:
        check_timeouts()
        requests = get_pending_requests()
        return render_template("index.html", requests=requests)
    except sqlite3.Error as e:
        flash(f"Database error: {e}")
        return render_template("index.html", requests=[])

@app.route("/resolve/<int:request_id>", methods=["POST"])
def resolve(request_id):
    try:
        answer = request.form.get("answer")
        if not answer:
            flash("Answer is required")
            return redirect(url_for("index"))
        question = resolve_help_request(request_id, answer)
        add_knowledge(question, answer)
        flash("Request resolved successfully")
        return redirect(url_for("index"))
    except sqlite3.Error as e:
        flash(f"Database error: {e}")
        return redirect(url_for("index"))

@app.route("/history")
def history():
    try:
        check_timeouts()
        requests = get_request_history()
        return render_template("history.html", requests=requests)
    except sqlite3.Error as e:
        flash(f"Database error: {e}")
        return render_template("history.html", requests=[])

@app.route("/learned")
def learned():
    try:
        knowledge = get_all_knowledge()
        return render_template("learned.html", knowledge=knowledge)
    except sqlite3.Error as e:
        flash(f"Database error: {e}")
        return render_template("learned.html", knowledge=[])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)