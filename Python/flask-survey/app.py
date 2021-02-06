from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "this-is-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

current_page = 0


@app.route('/')
def landing_page():
    return render_template('home.html')


@app.route('/begin')
def start_list():
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<quest_num>')
def questions_page(quest_num):
    global current_page
    quest_num = int(quest_num)
    if quest_num != current_page:
        flash("Invalid Question. Please answer the questions in order.", "error")
        return redirect('/questions/' + str(current_page))
    elif quest_num == len(surveys["satisfaction"].questions):
        return redirect('/thank-you')
    else:
        curr_quest_num = current_page
        title = surveys["satisfaction"].title
        instructions = surveys["satisfaction"].instructions
        question = surveys["satisfaction"].questions[quest_num]
        return render_template('questions.html', quest_num=curr_quest_num, title=title, instructions=instructions, question=question)


@app.route('/answer')
def answer():
    global current_page
    current_page += 1
    answer = request.args["question-form"]
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    return redirect('/questions/' + str(current_page))


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')
