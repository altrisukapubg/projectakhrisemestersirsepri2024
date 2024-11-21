from flask import Flask, render_template, request, redirect, session
import mysql.connector


app = Flask(__name__)
app.secret_key = "your_secret_key"


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restoran"
)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and (user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/dashboard")
        return "Login gagal. Username atau password salah.", 401
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return "Selamat datang di dashboard!"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)