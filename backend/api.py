from flask import Flask, request, jsonify
from query_data import query_rag
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis React

@app.route("/api/query", methods=["POST"])
def query():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question'"}), 400

    question = data["question"]
    try:
        response = query_rag(question)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
