from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db
from requests import get_pending_requests, resolve_help_request, get_request_history, check_timeouts
from knowledge import get_all_knowledge, add_knowledge
from agent import handle_call
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def index():
    try:
        check_timeouts()
        requests = get_pending_requests()
        return render_template("index.html", requests=requests)
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "error")
        return render_template("index.html", requests=[])

@app.route("/simulate_call", methods=["POST"])
def simulate_call():
    try:
        question = request.form.get("question")
        caller_id = request.form.get("caller_id")
        if not question or not caller_id:
            flash("Question and Caller ID are required", "error")
            return redirect(url_for("index"))
        handle_call(question, caller_id)
        flash("Call simulated successfully", "success")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Error simulating call: {e}", "error")
        return redirect(url_for("index"))

@app.route("/resolve/<int:request_id>", methods=["POST"])
def resolve(request_id):
    try:
        answer = request.form.get("answer")
        if not answer:
            flash("Answer is required", "error")
            return redirect(url_for("index"))
        question = resolve_help_request(request_id, answer)
        add_knowledge(question, answer)
        flash("Request resolved successfully", "success")
        return redirect(url_for("index"))
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("index"))

@app.route("/history")
def history():
    try:
        check_timeouts()
        requests = get_request_history()
        return render_template("history.html", requests=requests)
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "error")
        return render_template("history.html", requests=[])

@app.route("/learned")
def learned():
    try:
        knowledge = get_all_knowledge()
        return render_template("learned.html", knowledge=knowledge)
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "error")
        return render_template("learned.html", knowledge=[])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)