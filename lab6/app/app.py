"""
A Flask application to serve web pages for a Demon Slayer fan site.

This module configures a Flask application with routes to different pages
of a fan site for the anime Demon Slayer. Each route provides information 
about different aspects of the series, including characters and concepts. 
Logging is configured to record application activity.

Attributes:
    app (Flask): An instance of the Flask class.
"""

import logging
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Logging configuration
logging.basicConfig(filename='logs/app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

@app.route("/")
def index():
    """
    Render the index page of the Demon Slayer fan site.

    Logs the action and passes the current time to the template.

    Returns:
        A rendered template for the index page including the current time.
    """
    app.logger.info('Rendering index page')
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
    app.logger.info('Rendering overview page')
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
    app.logger.info('Rendering hashira page')
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
    app.logger.info('Rendering demon page')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("demon.html", current_time=time_now)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
