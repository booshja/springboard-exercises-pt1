from flask import Flask, request, render_template
from stories import story

app = Flask(__name__)


@app.route('/')
def home():
    """Displays landing page for the site"""

    return render_template('questions.html', words_list=story.prompts)


@app.route('/story')
def story_display():
    """Displays the rendered story from the user's input"""
    answers = request.args
    madlib = story.generate(answers)
    return render_template('story_display.html', madlib=madlib)
