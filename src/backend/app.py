import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'asl_model.pkl')
model = joblib.load(MODEL_PATH)


@app.route('/')
def health():
    return jsonify({'status': 'running'})


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'landmarks' not in data:
        return jsonify({'error': 'Missing landmarks data'}), 400

    landmarks = data['landmarks']

    # Expect 63 values (21 landmarks × 3 coords)
    if len(landmarks) != 63:
        return jsonify({'error': f'Expected 63 landmark values, got {len(landmarks)}'}), 400

    features = np.array(landmarks).reshape(1, -1)
    prediction = model.predict(features)[0]
    confidence = float(np.max(model.predict_proba(features)))

    return jsonify({'letter': prediction, 'confidence': round(confidence, 3)})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
