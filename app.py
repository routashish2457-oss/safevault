from flask import Flask, request, session, redirect, url_for
from auth import login_required, role_required
from database import get_db
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "secure-secret-key"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        return "Invalid credentials"

    return "Login Page"

@app.route("/dashboard")
@login_required
def dashboard():
    return "User Dashboard"

@app.route("/admin")
@login_required
@role_required("admin")
def admin():
    return "Admin Panel"

@app.route("/profile")
def profile():
    name = escape(request.args.get("name", "Guest"))
    return f"Welcome {name}"

if __name__ == "__main__":
    app.run(debug=True)
