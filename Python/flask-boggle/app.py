from boggle import Boggle
from flask import Flask, render_template, session, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "boggleSecretKey99"
# debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def landing_page():
    """Displays the homepage"""
    return render_template('home.html', css='home.css')


@app.route('/game')
def game_board():
    """Handles displaying the game itself"""
    board = boggle_game.make_board()
    session['board'] = board
    games = session.get('games', 0)
    high_score = session.get('high-score', 0)
    return render_template('game_board.html', css='game_board.css', games=games, high_score=high_score)


@app.route('/rules-gameplay')
def rules_gameplay_page():
    """Handles the rules and game play page"""
    return render_template('rules.html', css='rules.css')


@app.route('/game/word-guess')
def check_word():
    """Checks if the word submitted exists in the words file"""
    word = request.args['word']
    res = {"result": boggle_game.check_valid_word(session['board'], word)}
    return jsonify(res)


@app.route('/game/update', methods=["POST"])
def update_scores():
    """Handles updating the games played, and checking/updating of the high score"""
    games = session.get('games', 0)
    high_score = session.get('high-score', 0)
    score = request.json['score']
    session['games'] = games + 1
    session['high-score'] = max(score, high_score)

    return jsonify(new_record=score > high_score)
