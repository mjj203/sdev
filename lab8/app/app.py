"""
A Flask web application for a Demon Slayer fan site.

This module sets up a Flask application to manage user authentication and render 
different pages of a fan site dedicated to the anime Demon Slayer. It includes 
features for user registration and login, with routes to display information 
about the anime, such as an overview, details about Hashira, and demons. The 
application ensures secure access to certain pages, requiring users to log in 
before accessing restricted content.

The module configures logging and initializes a SQLite database to store user 
credentials. Password complexity checks are enforced during registration, and 
hashed passwords are stored in the database for security.

Functions:
    check_password_complexity: Validate password complexity.
    register: Handle user registration.
    login: Authenticate users and manage sessions.
    require_login: Restrict access to certain routes for non-authenticated users.
    index: Render the index page.
    overview: Render an overview page about Demon Slayer.
    hashira: Render a page about the Hashira in Demon Slayer.
    demon: Render a page about the demons in Demon Slayer.
    init_db: Initialize the application's SQLite database.

Running this script directly starts the Flask application.
"""

# Standard library imports
from datetime import datetime
import logging
import os
import re
import secrets
import sqlite3

# Related third-party imports
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
)

app.secret_key = secrets.token_hex(32)  # Set a secret key for session management


# Password complexity check function
def check_password_complexity(password):
    """
    Check the complexity of a given password.

    Validates the password against several criteria: length (must be at least 
    12 characters), inclusion of lowercase and uppercase letters, inclusion 
    of digits, and inclusion of special characters (underscore, at sign, or 
    dollar sign).

    Args:
        password (str): The password string to be checked.

    Returns:
        bool: True if the password meets all complexity requirements, False otherwise.
    """
    if len(password) < 12:
        logging.warning("Password complexity check failed: Length less than 12 characters")
        return False

    complexity_criteria = [
        ('[a-z]', "lowercase letter"),
        ('[A-Z]', "uppercase letter"),
        ('[0-9]', "digit"),
        ('[_@$]', "special character (_, @, $)")
    ]

    for pattern, criterion in complexity_criteria:
        if not re.search(pattern, password):
            logging.warning("Password complexity check failed: missing %s", criterion)
            return False

    return True

def is_common_password(password):
    """
    Check if the given password is a common password.

    This function reads a list of common passwords from a file named 'CommonPasswords.txt'
    and checks if the provided password is in that list. This is part of the security 
    measure to prevent users from choosing passwords that are easy to guess or have been 
    compromised in widespread data breaches.

    Args:
        password (str): The password to be checked against the list of common passwords.

    Returns:
        bool: True if the password is found in the list of common passwords, 
              False otherwise.

    Notes:
        The file 'CommonPasswords.txt' should be present in the same directory as this 
        function or in a specified path. The file should contain one password per line.
    """
    with open("CommonPassword.txt", "r", encoding="utf-8") as file:
        common_passwords = file.read().splitlines()
    return password in common_passwords


@app.route("/update_password", methods=["GET", "POST"])
def update_password():
    """
    Handle the password update process for a logged-in user.

    This route function allows a logged-in user to update their password. It presents 
    a form for the user to enter their current and new passwords when accessed via a 
    GET request. On a POST request, it processes the form data, validates the user's 
    current password, checks the complexity and commonality of the new password, and 
    updates the password in the database if all validations pass.

    The function ensures that:
    - The user is logged in before accessing the password update form.
    - The current password entered by the user matches the one stored in the database.
    - The new password meets predefined complexity criteria and is not commonly used.

    If any validation fails, appropriate feedback is provided to the user.

    Returns:
        On GET request: Renders the 'update_password.html' template.
        On POST request: Redirects to the index page if the password update is 
                         successful, or re-renders 'update_password.html' with 
                         an appropriate message if not.

    Raises:
        sqlite3.DatabaseError: If there's an error during database operations.
    """
    if 'user' not in session:
        flash("Please log in to update your password")
        return redirect(url_for("login"))

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]

        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username = ?", (session["user"],))
            user = cur.fetchone()

            if user and check_password_hash(user[0], current_password):
                if not check_password_complexity(new_password):
                    flash("New password does not meet complexity requirements")
                elif is_common_password(new_password):
                    flash("New password is too common, please choose a different one")
                else:
                    hashed_new_password = generate_password_hash(new_password)
                    current_time = datetime.now()
                    cur.execute(
                        "UPDATE users SET password = ?, last_password_update = ? "
                        "WHERE username = ?",
                        (hashed_new_password, current_time, session["user"])
                    )
                    conn.commit()
                    flash("Password successfully updated")
                    return redirect(url_for("index"))
            else:
                flash("Current password is incorrect")

        except sqlite3.DatabaseError as db_err:
            logging.error("Database error in update_password function: %s", db_err)
            flash("An error occurred. Please try again later.")
        finally:
            conn.close()

    return render_template("update_password.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user to the system.

    On a GET request, this route presents the registration form. On a POST 
    request, it processes the submitted registration form. The function 
    checks if the provided password meets the complexity requirements and 
    then attempts to register the new user in the 'users' database. The 
    password is hashed before storing for security.

    If the chosen username is already in use or the password doesn't meet 
    the complexity requirements, the user is informed via a flash message.
    Upon successful registration, the user is redirected to the login page.

    Returns:
        On GET request: Renders the 'register.html' template.
        On POST request: Redirects to the login page if registration is 
                         successful, or re-renders 'register.html' with 
                         an appropriate message if not.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if is_common_password(password):
            flash("Password is too common, please choose a different one")
            return render_template("register.html")

        if not check_password_complexity(password):
            flash("Password does not meet complexity requirements")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)
        current_time = datetime.now()

        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, last_password_update) VALUES (?, ?, ?)",
                (username, hashed_password, current_time)
            )
            conn.commit()
            logging.info("New user registered: %s", username)
        except sqlite3.IntegrityError:
            logging.warning("Registration failed: Username %s already taken", username)
            flash("Username already taken")
            return render_template("register.html")
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate a user and initiate a session.

    This route handles both the display of the login form (on GET request) and 
    the processing of login credentials (on POST request). When credentials are 
    posted, it checks the provided username and password against the stored 
    values in the 'users' database. If authentication is successful, the user's 
    username is stored in the session, and they are redirected to the index page.
    Otherwise, a message flashes indicating invalid credentials.

    Returns:
        On GET request: Renders the 'login.html' template.
        On POST request: Redirects to the index page if login is successful, or
                         re-renders 'login.html' with an error message if not.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
            conn.close()

            if user and check_password_hash(user[0], password):
                logging.info("User logged in: %s", username)
                session["user"] = username
                return redirect(url_for("index"))
            # Log the failed login attempt with date, time, and IP address
            logging.warning(
                "Failed login attempt for username: %s. IP: %s", 
                username,
                request.remote_addr
            )
            flash("Invalid username or password")
        except sqlite3.DatabaseError as db_err:
            logging.error("Database error in login function: %s", db_err)
            flash("An error occurred. Please try again later.")

    return render_template("login.html")


@app.before_request
def require_login():
    """
    Restrict access to certain pages for non-authenticated users.

    This function runs before each request. It checks if a user is logged in 
    by looking for 'user' in the session. If the user is not logged in and 
    attempts to access routes other than 'login' and 'register', they are 
    redirected to the login page.

    This ensures that only authenticated users can access certain parts of 
    the application.
    """
    allowed_routes = ["login", "register"]
    if "user" not in session and request.endpoint not in allowed_routes:
        logging.info(
            "Non-authenticated access attempt to %s. IP: %s", 
            request.endpoint,
            request.remote_addr
        )
        return redirect(url_for("login"))

    return None


@app.route("/")
def index():
    """
    Render the index page of the Demon Slayer fan site.

    Logs the action and passes the current time to the template.

    Returns:
        A rendered template for the index page including the current time.
    """
    app.logger.info("Rendering index page")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("index.html", current_time=time_now)


@app.route("/overview")
def overview():
    """
    Render the overview page of the Demon Slayer fan site.

    Logs the action and passes the current time to the template.

    Returns:
        A rendered template for the overview page including the current time.
    """
    app.logger.info("Rendering overview page")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("overview.html", current_time=time_now)


@app.route("/hashira")
def hashira():
    """
    Render the hashira page of the Demon Slayer fan site.

    Logs the action and passes the current time to the template.

    Returns:
        A rendered template for the hashira page including the current time.
    """
    app.logger.info("Rendering hashira page")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("hashira.html", current_time=time_now)


@app.route("/demon")
def demon():
    """
    Render the demon page of the Demon Slayer fan site.

    Logs the action and passes the current time to the template.

    Returns:
        A rendered template for the demon page including the current time.
    """
    app.logger.info("Rendering demon page")
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("demon.html", current_time=time_now)


def init_db():
    """
    Initialize the application's database.

    Checks for the existence of 'users.db' and creates it if not present, along
    with a 'users' table. The 'users' table includes 'id' (primary key),
    'username' (unique), and 'password'. Errors during database operations are
    logged, and the function ensures closure of the database connection.

    Raises:
        sqlite3.Error: If any database operations fail.
    """
    db_exists = os.path.exists("users.db")

    try:
        if not db_exists:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    last_password_update DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.info("Database created and initialized")
        else:
            logging.info("Database already exists")
    except sqlite3.Error as err:
        logging.error("Database error: %s", err)
        raise
    finally:
        if not db_exists:
            conn.close()


if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(host="127.0.0.1", port=8080)
