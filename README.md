# 🧠 AutoDQ — Declarative Data Quality Validation Engine

> **Aneerban Chowdhury, M.Tech (Data Engineering), IIT Jodhpur**

AutoDQ is a **Flask-based Data Quality Validation Engine** designed to perform **rule-driven validation** on structured datasets (e.g., KYC and Credit Card data).  
It provides a simple **web interface** for Login/Signup, Data Selection, Rule Execution, and Data Inspection — empowering data engineers and analysts to validate datasets in a declarative way using **YAML rule definitions**.

---

## 🚀 Key Features

| Feature | Description |
|----------|-------------|
| 🔐 **Login / Signup** | Secure user management using SQLite + hashed passwords |
| 🧩 **Dataset Selection** | Choose between *KYC* and *Credit Card* datasets |
| 👁️ **Sample Data Preview** | View top N rows (up to 100) directly on UI |
| 🔍 **Customer Search** | Search by `customer_id` and view selected columns |
| 🧠 **DQ Rule Runner** | Run one, many, or all DQ rules on selected dataset |
| 📊 **Interactive Results** | See failed record counts and view full failed rows in a modal popup |
| ⚙️ **Declarative YAML Rules** | Define rules in a simple YAML format — no coding required |
| ☁️ **Cloud Ready** | Deploy easily on Render, GitHub, or any Flask-compatible platform |

---

## 🧮 Project Structure

```
📁 AutoDQ/
├── app.py                       # Flask main application
├── requirements.txt             # Dependencies list
├── users.db                     # SQLite user database (auto-created)
│
├── dq_engine/
│   ├── main_validator.py        # Core DQ validation engine
│   ├── data/
│   │   ├── kyc_data.csv
│   │   └── creditcard_data.csv
│   └── rules/
│       ├── kyc_rules.yaml
│       └── creditcard_rules.yaml
│
├── templates/
│   ├── login.html
│   ├── dataset_selection.html
│   ├── action_selection.html
│   ├── sample_preview.html
│   ├── customer_search.html
│   ├── dq_run.html
│   └── base.html
│
└── static/
    ├── css/
    └── js/
```

---

## ⚙️ Installation & Setup

### 🖥️ Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/aneerban10/mtech-project-autodq.git
   cd mtech-project-autodq
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate      # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000/
   ```

---

## ☁️ Deployment (Render or Cloud)

1. Push your project to GitHub:
   ```bash
   git add .
   git commit -m "Initial AutoDQ commit"
   git push origin main
   ```

2. Go to **[Render](https://render.com/)** → **New Web Service**

3. Configure:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. Once deployed, your app will be available at:
   ```
   https://autodq.onrender.com/
   ```

---

## 🧾 YAML Rule Example

Example from `kyc_rules.yaml`:

```yaml
rules:
  - name: "Validate KYC Type"
    column: "kyc_type"
    rule: "one_of"
    value: ["Aadhaar", "PAN", "Passport"]

  - name: "Expiry Date Validation"
    column: "kyc_expiry"
    rule: "date_greater_than_today"

  - name: "Customer ID Not Null"
    column: "customer_id"
    rule: "not_null"
```

✅ *Each rule defines column, condition, and validation type.*

---

## 🧩 Core Logic Highlights

### 🔹 Validation Engine (`main_validator.py`)

- Reads dataset (`CSV`) and YAML rules.
- Applies functions like:
  - `one_of()`
  - `not_null()`
  - `custom_regex()`
  - `alphanumeric()`
  - `date_greater_than_today()`
- Returns rule-wise failure counts and failed rows.

### 🔹 Flask UI (`app.py`)

- Routes:
  - `/` → Login / Signup  
  - `/dataset_selection` → Choose dataset  
  - `/sample_preview` → View sample data  
  - `/customer_search` → Search by `customer_id`  
  - `/dq_run` → Run DQ Rules  

---

## 💡 Future Enhancements

- 🧱 Rule Dependency Graph  
- 🪄 YAML Auto-generator from Schema  
- ☁️ GCP/Azure Deployment  
- 📈 Dashboard with Validation Statistics  
- 🧬 Integration with Data Lake or ADF  

---

## 👨‍💻 Author

**Aneerban Chowdhury**  
M.Tech (Data Engineering) | IIT Jodhpur  
📫 [aneerban10@gmail.com](mailto:aneerban10@gmail.com)  
🔗 [GitHub: aneerban10](https://github.com/aneerban10)

---

## 🏁 License

This project is open-sourced under the **MIT License**.

⭐ *If you found this project useful, don’t forget to give it a star on GitHub!* 🌟
