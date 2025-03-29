import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="templates")  
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY, 
                          username TEXT UNIQUE, 
                          password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                          id INTEGER PRIMARY KEY, 
                          name TEXT UNIQUE, 
                          timing TEXT, 
                          seats INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                          id INTEGER PRIMARY KEY, 
                          user TEXT, 
                          movie TEXT, 
                          seats INTEGER, 
                          seat_numbers TEXT)''')
        
        # Add sample movies if not exists
        sample_movies = [
            ("Avengers: Endgame", "7:00 PM", 50),
            ("Interstellar", "8:30 PM", 30),
            ("Inception", "9:15 PM", 40)
        ]
        for movie in sample_movies:
            cursor.execute("SELECT * FROM movies WHERE name=?", (movie[0],))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO movies (name, timing, seats) VALUES (?, ?, ?)", movie)
        conn.commit()

@app.route("/")
def home():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
    return render_template("index.html", movies=movies)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect(url_for('home'))
        return "Invalid credentials. Try again."
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                return "Error: Username already exists."
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/book/<int:movie_id>", methods=['GET', 'POST'])
def book(movie_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,))
        movie = cursor.fetchone()
    if request.method == 'POST':
        selected_seats = request.form['selectedSeats']
        seat_count = len(selected_seats.split(",")) if selected_seats else 0
        if seat_count == 0:
            return "Please select at least one seat."
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT seats FROM movies WHERE id=?", (movie_id,))
            available_seats = cursor.fetchone()[0]
            if seat_count > available_seats:
                return "Error: Not enough seats available."
            cursor.execute("INSERT INTO bookings (user, movie, seats, seat_numbers) VALUES (?, ?, ?, ?)",
                           (session['user'], movie[1], seat_count, selected_seats))
            cursor.execute("UPDATE movies SET seats = seats - ? WHERE id = ?", (seat_count, movie_id))
            conn.commit()
        return redirect(url_for('receipt', movie_id=movie_id, seats=selected_seats))
    return render_template("book.html", movie=movie)

@app.route("/receipt/<int:movie_id>/<seats>")
def receipt(movie_id, seats):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,))
        movie = cursor.fetchone()
    return render_template("receipt.html", movie=movie, seats=seats)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
