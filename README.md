# Movie Ticket Booking System

## Introduction
This is a simple movie ticket booking system built using Flask (Python) for the backend and HTML/CSS for the frontend. Users can register, log in, browse available movies, and book tickets.

## Features
- User authentication (Register/Login/Logout)
- Movie listing with available seats
- Ticket booking system
- SQLite database for data storage

## Installation
### Prerequisites
- Python 3.x installed
- Flask installed

### Setup Instructions
1. Clone the repository or download the files.
2. Navigate to the project directory.
3. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Initialize the database:
   ```sh
   python app.py
   ```
   This will create an SQLite database file (`database.db`).
6. Run the application:
   ```sh
   python app.py
   ```
7. Open your browser and go to `http://127.0.0.1:5000/` to use the system.

## File Structure
```
movie_booking/
│── static/
│   ├── style.css
│── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── book.html
│── database.db
│── app.py
│── requirements.txt
│── README.md
```

## Usage
- Register a new account.
- Log in to access the system.
- Browse available movies and select one to book tickets.
- Enter the number of tickets and confirm booking.
- Logout when done.

## Technologies Used
- Python (Flask Framework)
- SQLite (Database)
- HTML/CSS (Frontend)

## License
This project is open-source. You are free to modify and distribute it.

## Author
Developed by [Your Name]

