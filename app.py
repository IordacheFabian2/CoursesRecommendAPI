import os
from flask import Flask, request, jsonify
from model import get_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return "Udemy Courses API"

@app.route('/recommend', methods=['GET'])
def recommend():
    role = request.args.get('role')
    if not role:
        return jsonify({'error': 'Missing `role` parameter'}), 400

    courses = get_recommendations(role)
    if not courses:
        return jsonify({'error': f'No recommendations found for role: {role}'}), 404

    return jsonify({'role': role, 'recommendations': courses})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # default fallback
    app.run(host='0.0.0.0', port=port)
