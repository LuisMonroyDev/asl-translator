from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def health():
    return jsonify({'status': 'running'})


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'landmarks' not in data:
        return jsonify({'error': 'Missing landmarks data'}), 400

    return jsonify({'letter': 'A', 'confidence': 0.95})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
