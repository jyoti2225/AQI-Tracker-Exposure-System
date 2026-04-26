from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import oracledb
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "aqi_project_secret"

def get_connection():
    return oracledb.connect(
        user="system",
        password="your_password",
        dsn="localhost:1521/XEPDB1"
    )

@app.route("/")
def home():
    username = session.get("username")
    return render_template("dashboard.html", username=username)

@app.route("/login")
def login_page():
    logged_out = request.args.get("logged_out")
    return render_template("login.html", logged_out=logged_out)


@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login_check", methods=["POST"])
def login_check():
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT USER_ID, USERNAME, EMAIL, PASSWORD, ROLE
            FROM USERS
            WHERE USERNAME = :1 AND EMAIL = :2 AND PASSWORD = :3
        """, [username, email, password])

        user = cursor.fetchone()

        cursor.close()
        conn.close()

    except Exception as e:
        return f"Database error: {e}"

    if user:
        session["username"] = user[1]
        session["email"] = user[2]
        session["role"] = user[4]
        return redirect(url_for("home"))
    else:
        return "Invalid login details"

@app.route("/signup_check", methods=["POST"])
def signup_check():
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    if not username or not email or not password:
        return "All fields are required"

    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#^()_+\-=\[\]{};\'":\\|,.<>\/?])[A-Za-z\d@$!%*?&.#^()_+\-=\[\]{};\'":\\|,.<>\/?]{8,}$'

    if not re.match(email_pattern, email):
        return "Invalid email format"

    if not re.match(password_pattern, password):
        return "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM USERS
            WHERE USERNAME = :1 OR EMAIL = :2
        """, [username, email])

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return "Username or Email already exists"

        cursor.execute("""
            INSERT INTO USERS (USERNAME, EMAIL, PASSWORD, ROLE)
            VALUES (:1, :2, :3, :4)
        """, [username, email, password, "user"])

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("login_page"))

    except Exception as e:
        return f"Database error: {e}"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/healthadvisory")
def health():
    return render_template("healthadvisory.html")

@app.route("/exposure")
def exposure():
    if "username" not in session:
        return redirect(url_for("login_page"))
    return render_template("exposure.html")

@app.route("/admin")
def admin_page():
    if "username" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "admin":
        return "Access denied"

    return render_template("admin.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page", logged_out=1))

@app.route("/test")
def test():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM AQI_DATA ORDER BY CREATED_AT ASC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return str(data)

@app.route("/get_aqi")
def get_aqi():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM AQI_DATA ORDER BY CREATED_AT ASC")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    data = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(data)

@app.route("/get_cities")
def get_cities():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT CITY_ID, CITY_NAME FROM CITIES ORDER BY CITY_ID")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            "CITY_ID": row[0],
            "CITY_NAME": row[1]
        })

    cursor.close()
    conn.close()

    return jsonify(data)

@app.route("/api/city_data")
def api_city_data():
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "City is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT CITY_ID, CITY_NAME
            FROM CITIES
            WHERE UPPER(CITY_NAME) = UPPER(:1)
        """, [city])

        city_row = cursor.fetchone()

        if not city_row:
            return jsonify({"error": "City not found"}), 404

        city_id = city_row[0]
        city_name = city_row[1]

        cursor.execute("""
            SELECT AQI, TEMPERATURE, RAIN, UV, CREATED_AT
            FROM AQI_DATA
            WHERE CITY_ID = :1
            ORDER BY CREATED_AT ASC
        """, [city_id])

        rows = cursor.fetchall()

        if not rows:
            return jsonify({"error": "No AQI data found for this city"}), 404

        current_hour = datetime.now().hour

        if len(rows) >= 24:
            current = rows[current_hour]
        else:
            current = rows[-1]

        data = {
            "city": city_name,
            "current": {
                "aqi": float(current[0]) if current[0] is not None else 0,
                "temperature": float(current[1]) if current[1] is not None else 0,
                "rain": float(current[2]) if current[2] is not None else 0,
                "uv": float(current[3]) if current[3] is not None else 0
            },
            "hourly": {
                "time": [str(row[4]) for row in rows],
                "aqi": [float(row[0]) if row[0] is not None else 0 for row in rows],
                "temperature": [float(row[1]) if row[1] is not None else 0 for row in rows],
                "rain": [float(row[2]) if row[2] is not None else 0 for row in rows],
                "uv": [float(row[3]) if row[3] is not None else 0 for row in rows]
            }
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    app.run(debug=True)