"""
Flask Endpoint Tests
====================
Verifies that the Flask server handles requests correctly.

Prerequisites:
    1. Virtual environment activated: source venv/bin/activate
    2. Dependencies installed: pip install -r requirements.txt

Run tests:
    python -m pytest tests/test_flask_endpoint.py -v

What these tests check:
    - test_predict_valid_input: 63 landmarks returns a letter prediction
    - test_predict_missing_landmarks: No landmarks field returns 400 error
    - test_predict_wrong_count: Wrong number of landmarks returns 400 error
    - test_predict_no_json: Request without JSON body returns 415 error
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))
from app import app


class TestPredictEndpoint(unittest.TestCase):

    def setUp(self):
        """Create a test client before each test."""
        app.testing = True
        self.client = app.test_client()

    def test_predict_valid_input(self):
        """POST /predict with landmarks returns a letter and confidence."""
        # 21 landmarks × 3 coordinates (x, y, z) = 63 values
        landmarks = [0.0] * 63
        response = self.client.post('/predict', json={'landmarks': landmarks})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('letter', data)
        self.assertIn('confidence', data)
        self.assertEqual(data['letter'], 'A')
        self.assertEqual(data['confidence'], 0.95)

    def test_predict_missing_landmarks(self):
        """POST /predict without landmarks field returns 400."""
        response = self.client.post('/predict', json={'wrong_key': []})

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_predict_no_json(self):
        """POST /predict without JSON body returns 415 (Unsupported Media Type)."""
        response = self.client.post('/predict', data='not json')

        self.assertEqual(response.status_code, 415)

    def test_predict_empty_body(self):
        """POST /predict with empty body returns 400."""
        response = self.client.post('/predict',
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()