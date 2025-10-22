from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
import pandas as pd
from dq_engine.dq_runner import run_validation, get_available_columns, load_rules_yaml

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_PATH = "users.db"

# ------------------- Database Setup -------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
init_db()

# ------------------- Routes -------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect(DB_PATH) as conn:
            user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect(url_for("select_dq"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        return render_template("login.html", success="Signup successful! Please login.")
    except sqlite3.IntegrityError:
        return render_template("login.html", error="Username already exists.")

@app.route("/select_dq", methods=["GET", "POST"])
def select_dq():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        dq_type = request.form["dq_type"]
        row_limit = int(request.form["row_limit"])
        selected_rule = request.form.get("rule_name")

        # Load corresponding file paths
        yaml_path = f"dq_engine/yaml/{dq_type}_rules.yaml"
        data_path = f"dq_engine/data/{dq_type}_data.csv"

        df = pd.read_csv(data_path).head(row_limit)
        rules = load_rules_yaml(yaml_path)
        columns = list(df.columns)

        if "run_all" in request.form:
            results = run_validation(data_path, yaml_path)
        elif selected_rule:
            results = run_validation(data_path, yaml_path, selected_rule=selected_rule)
        else:
            results = []

        return render_template(
            "results.html",
            dq_type=dq_type,
            data=df.to_html(classes="data-table", index=False),
            rules=rules,
            results=results,
            columns=columns
        )

    return render_template("select_dq.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
