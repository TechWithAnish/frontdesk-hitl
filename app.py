from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from requests import get_pending_requests, resolve_help_request

app = Flask(__name__)

@app.route("/")
def index():
         requests = get_pending_requests()
         return render_template("index.html", requests=requests)

@app.route("/resolve/<int:request_id>", methods=["POST"])
def resolve(request_id):
         answer = request.form["answer"]
         resolve_help_request(request_id, answer)
         return redirect(url_for("index"))

if __name__ == "__main__":
         init_db()
         app.run(debug=True)