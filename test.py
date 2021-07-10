from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Time left:', res.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                ["C", "A", "T", "T", "T"], 
                                ["C", "A", "T", "T", "T"], 
                                ["C", "A", "T", "T", "T"], 
                                ["C", "A", "T", "T", "T"]]
        res = self.client.get('/check-word?word=cat')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        res = self.client.get('/check-word?word=impossible')
        self.assertEqual(res.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        res = self.client.get(
            '/check-word?word=asfsafdsdfasf')
        self.assertEqual(rese.json['result'], 'not-word')
