#!/usr/bin/python3
""" Web server
"""
from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def index():
    """ Root
    """
    return redirect(url_for('redirect_1'), code=301)

@app.route("/redirect_1", strict_slashes=False)
def redirect_1():
    """ redirect_1
    """
    return "With one redirection"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)