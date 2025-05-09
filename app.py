from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from requests import get_pending_requests, resolve_help_request, get_request_history
from knowledge import get_all_knowledge, add_knowledge

app = Flask(__name__)

@app.route("/")
def index():
    requests = get_pending_requests()
    return render_template("index.html", requests=requests)

@app.route("/resolve/<int:request_id>", methods=["POST"])
def resolve(request_id):
    answer = request.form["answer"]
    question = resolve_help_request(request_id, answer)
    add_knowledge(question, answer)
    return redirect(url_for("index"))

@app.route("/history")
def history():
    requests = get_request_history()
    return render_template("history.html", requests=requests)

@app.route("/learned")
def learned():
    knowledge = get_all_knowledge()
    return render_template("learned.html", knowledge=knowledge)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)