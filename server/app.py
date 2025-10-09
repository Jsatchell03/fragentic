import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route("/search", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("message", "").strip()

    if not query:
        return jsonify({"reply": "⚠️ No input received."}), 400

    try:
        reply_text = recommend_text(query)
        return jsonify({"reply": reply_text})
    except Exception as e:
        return jsonify({"reply": f"❌ Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
