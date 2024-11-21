from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db = mysql.connector.connect(
    host=app.config["DB_HOST"],
    user=app.config["DB_USER"],
    password=app.config["DB_PASSWORD"],
    database=app.config["DB_NAME"]
)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"] 

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:  
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/menu")
        else:
            return render_template("login.html", error="Username atau password salah.")
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/menu')
def menu():
    if "user_id" not in session:
        return redirect('/login')

    cursor = db.cursor()
    cursor.execute("SELECT * FROM menu")
    data = cursor.fetchall()
    cursor.close()
    return render_template('menu.html', data=data)

@app.route('/tambah', methods=["POST", "GET"])
def tambah():
    if "user_id" not in session:
        return redirect('/login')

    if request.method == "POST":
        cursor = db.cursor()
        nama_menu = request.form["nama_menu"]
        harga = request.form["harga"]
        deskripsi = request.form["deskripsi"]
        query = "INSERT INTO menu (id, nama_menu, harga, deskripsi) VALUES (%s, %s, %s, %s)"
        data = (None, nama_menu, harga, deskripsi)
        cursor.execute(query, data)
        db.commit()
        cursor.close()
        return redirect("/menu")
    return render_template("tambah.html")

@app.route('/hapus/<id>')
def hapus(id):
    if "user_id" not in session:
        return redirect('/login')

    cursor = db.cursor()
    query = "DELETE FROM menu WHERE id = %s"
    data = (id,)
    cursor.execute(query, data)
    db.commit()
    cursor.close()
    return redirect('/menu')

@app.route('/edit/<id>', methods=["GET", "POST"])
def edit(id):
    if "user_id" not in session:
        return redirect('/login')

    cursor = db.cursor()
    if request.method == "POST":
        nama_menu = request.form["nama_menu"]
        harga = request.form["harga"]
        deskripsi = request.form["deskripsi"]
        query = "UPDATE menu SET nama_menu = %s, harga = %s, deskripsi = %s WHERE id = %s"
        data = (nama_menu, harga, deskripsi, id)
        cursor.execute(query, data)
        db.commit()
        cursor.close()
        return redirect('/menu')
    else:
        query = "SELECT * FROM menu WHERE id = %s"
        data = (id,)
        cursor.execute(query, data)
        value = cursor.fetchone()
        cursor.close()
        return render_template('edit.html', value=value)

if __name__ == "__main__":
    app.run(debug=True)