from flask import Flask, render_template, request, redirect, url_for,session
from dq_engine.main_validator import run_all_rules, run_single_rule
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_PATH = "users.db"

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


# ---------------- LOGIN/SIGNUP ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    success = request.args.get("success")
    if request.method == "POST":
        username = request.form['userid']
        pwd = request.form['password']

        with sqlite3.connect(DB_PATH) as conn:
            user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

        if user and check_password_hash(user[2], pwd):
            session["user"] = username
            return redirect(url_for("dataset_selection"))
        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error, success=success)


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["userid"]
    pwd = generate_password_hash(request.form["password"])

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, pwd))
        # Pass success message as query param to login page
        return redirect(url_for("login", success="Signup successful! Please login."))
    except sqlite3.IntegrityError:
        return render_template("login.html", error="Username already exists.")


# ---------------- DATASET SELECTION ----------------
@app.route("/dataset_selection", methods=["GET", "POST"])
def dataset_selection():
    if request.method == "POST":
        dataset = request.form['dataset']
        return redirect(url_for("action_selection", dataset=dataset))
    return render_template("dataset_selection.html")

# ---------------- ACTION SELECTION ----------------
@app.route("/action_selection/<dataset>")
def action_selection(dataset):
    return render_template("action_selection.html", dataset=dataset)

# ---------------- SAMPLE PREVIEW ----------------
@app.route("/sample_preview/<dataset>", methods=["GET", "POST"])
def sample_preview(dataset):
    data_path = f"dq_engine/data/{dataset}_data.csv"
    df = pd.read_csv(data_path)
    n_rows = int(request.form.get("n_rows", 5))
    table_html = df.head(n_rows).to_html(classes="table table-striped", index=False)
    return render_template("sample_preview.html", data=table_html, dataset=dataset)

# ---------------- CUSTOMER SEARCH ----------------
@app.route("/customer_search/<dataset>", methods=["GET", "POST"])
def customer_search(dataset):
    data_path = f"dq_engine/data/{dataset}_data.csv"
    df = pd.read_csv(data_path)
    result_table = None
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        selected_cols = request.form.getlist("columns")
        if customer_id:
            result_df = df[df['customer_id'] == customer_id]
            if selected_cols:
                result_df = result_df[selected_cols]
            result_table = result_df.to_html(classes="table table-striped", index=False)
    return render_template("customer_search.html", table=result_table, dataset=dataset, columns=df.columns)

# ---------------- DQ RULE RUN ----------------
@app.route("/dq_run/<dataset>", methods=["GET", "POST"])
def dq_run(dataset):
    rules_path = f"dq_engine/rules/{dataset}_rules.yaml"
    import yaml
    with open(rules_path) as f:
        rules_yaml = yaml.safe_load(f)
    rules_list = [rule["name"] for rule in rules_yaml["rules"]]

    results = None
    if request.method == "POST":
        selected_rules = request.form.getlist("rules")
        from dq_engine.main_validator import run_validation
        data_path = f"dq_engine/data/{dataset}_data.csv"
        if "All Rules" in selected_rules:
            results = run_validation(data_path, rules_path)
        else:
            results = []
            for r in selected_rules:
                res = run_single_rule(data_path, rules_path, r)
                results.extend(res)
    return render_template("dq_run.html", rules=rules_list, results=results,dataset=dataset)

#if __name__ == "__main__":
#    app.run(debug=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT via environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
