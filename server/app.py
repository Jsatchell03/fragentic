import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import os

dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
frag_db = mongodb_client["fragrance_db"]

app = Flask(__name__)
CORS(app)
api = Api(app)


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
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
