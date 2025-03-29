import sqlite3

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        # Create Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create Movies Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timing TEXT NOT NULL,
                seats INTEGER NOT NULL
            )
        ''')

        # Create Bookings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                movie TEXT NOT NULL,
                seats INTEGER NOT NULL
            )
        ''')

        # Insert Multiple Movies
        cursor.executemany('''
            INSERT INTO movies (name, timing, seats) VALUES (?, ?, ?)
        ''', [
            ("Avengers: Endgame", "7:00 PM", 50),
            ("Interstellar", "8:30 PM", 30),
            ("Inception", "9:15 PM", 40),
            ("Spider-Man: No Way Home", "6:30 PM", 35),
            ("The Dark Knight", "9:00 PM", 45),
            ("Joker", "8:00 PM", 25),
            ("Titanic", "5:00 PM", 50),
            ("Fast & Furious 9", "10:00 PM", 40),
            ("Black Panther", "7:45 PM", 30),
            ("Doctor Strange", "6:00 PM", 20)
        ])

        conn.commit()
    
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
