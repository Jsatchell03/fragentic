import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
from openai import OpenAI
import os

dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

w_note_coverage, w_base_sim = 0.35, 0.65
frag_db = mongodb_client["fragrance_db"]

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route("/api/v1/search", methods=["POST"])
def search():
    data = request.get_json()  # Returns a dict
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    def embed_list(texts: list):
        ai_response = [
            x.embedding
            for x in client.embeddings.create(
                model="text-embedding-3-small", input=texts
            ).data
        ]
        return ai_response


@app.route("/api/v1/accords", methods=["GET"])
def get_accords():
    data = [{"name": x["name"]} for x in list(frag_db["accords"].find({}))]
    return jsonify(data)


@app.route("/api/v1/brands", methods=["GET"])
def get_brands():
    data = [{"name": x["name"]} for x in list(frag_db["brands"].find({}))]
    print(data)
    return jsonify(data)


@app.route("/api/v1/countries", methods=["GET"])
def get_countries():
    data = [{"name": x["name"]} for x in list(frag_db["countries"].find({}))]
    return jsonify(data)


@app.route("/api/v1/notes", methods=["GET"])
def get_notes():
    data = [{"name": x["name"]} for x in list(frag_db["notes"].find({}))]
    return jsonify(data)


@app.route("/api/v1/filters", methods=["GET"])
def get_filters():
    data = {}
    data["brands"] = [{"name": x["name"]} for x in list(frag_db["brands"].find({}))]
    data["countries"] = [
        {"name": x["name"]} for x in list(frag_db["countries"].find({}))
    ]
    data["notes"] = [{"name": x["name"]} for x in list(frag_db["notes"].find({}))]
    data["accords"] = [{"name": x["name"]} for x in list(frag_db["accords"].find({}))]
    data["descriptors"] = list(
        {x["name"] for x in data["notes"]} | {x["name"] for x in data["accords"]}
    )
    cursor = frag_db["fragrances"].find({}, {"ratingCount": 1, "_id": 0})
    df = pd.DataFrame(list(cursor))
    df = df.dropna(subset=["ratingCount"])
    quantiles = df["ratingCount"].quantile([0.2, 0.4, 0.6, 0.8])
    data["popularityCutoffs"] = list(quantiles.to_dict().values())
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
