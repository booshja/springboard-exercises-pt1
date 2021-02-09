from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_landing_page(self):
        """
        Tests:
        -status code
        -html is displayed
        """
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button>Rules and Gameplay</button>', html)

    def test_game_board(self):
        """
        Tests:
        -status code
        -html is displayed
        -session is updated
        """
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['games'] = 12
                change_session['high-score'] = 42

            res = client.get('/game')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 id="high-score">', html)
            self.assertEqual(session['games'], 12)
            self.assertEqual(session['high-score'], 42)

    def test_rules_gameplay_page(self):
        """
        Tests:
        -status code
        -html is displayed
        """
        with app.test_client() as client:
            res = client.get('/rules-gameplay')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Gameplay:</h3>', html)

    def test_check_word(self):
        """
        Tests:
        -status code
        -html is displayed
        -checks word and returns correct response
        """
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['A', 'B', 'C', 'D', 'E'], ['A', 'B', 'C', 'D', 'E'], [
                    'A', 'B', 'C', 'D', 'E'], ['A', 'B', 'C', 'D', 'E'], ['A', 'B', 'C', 'A', 'T']]
            res = client.get('/game/word-guess?word=cat')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'ok')
