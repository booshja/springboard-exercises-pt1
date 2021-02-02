from flask import Flask

app = Flask(__name__)


@app.route('/welcome')
def welcome():
    """displays 'welcome' on the screen"""
    return "welcome"


@app.route('/welcome/home')
def welcome_home():
    """displays 'welcome home' on the screen"""
    return "welcome home"


@app.route('/welcome/back')
def welcome_back():
    """displays 'welcome back' on the screen"""
    return "welcome back"
