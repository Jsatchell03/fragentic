import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import numpy as np
from openai import OpenAI
from scipy.spatial.distance import cosine, cdist
from bson import ObjectId


dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path)
mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

w_note_coverage, w_base_sim = 0.35, 0.65
frag_db = mongodb_client["fragrance_db"]
full_match, half_match, neg_match = 0.55, 0.45, 0.2

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route("/api/v1/search", methods=["POST"])
def search():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    if len(data["descriptors"]) == 0:
        return jsonify({"error": "Empty query received"}), 400

    print(data)

    def embed_list(texts: list):
        ai_response = [
            x.embedding
            for x in client.embeddings.create(
                model="text-embedding-3-small", input=texts
            ).data
        ]
        return ai_response

    def average_embeddings(vectors, weight=1.0):
        return weight * np.mean(vectors, axis=0)

    # def coverage(user_input_vectors, descriptor_ids, collection):
    #     if not descriptor_ids or not user_input_vectors:
    #         return 0.0

    #     descriptor_docs = list(
    #         collection.find({"_id": {"$in": descriptor_ids}}, {"embedding": 1})
    #     )

    #     if not descriptor_docs:
    #         return 0.0

    #     embeddings = np.array([doc["embedding"] for doc in descriptor_docs])

    #     user_vecs = np.array(user_input_vectors)

    #     similarity_matrix = 1 - cdist(user_vecs, embeddings, metric="cosine")

    #     full_mask = similarity_matrix >= full_match
    #     half_mask = (similarity_matrix >= half_match) & ~full_mask
    #     low_mask = similarity_matrix < neg_match
    #     penalties = np.zeros_like(similarity_matrix)
    #     penalties[low_mask] = neg_match - similarity_matrix[low_mask]

    #     matches = full_mask.sum() + 0.5 * half_mask.sum() - penalties.sum()

    #     return matches / ((len(descriptor_ids) * len(user_input_vectors)))

    input_descriptors_embedding = embed_list(data["descriptors"])
    input_embedding = average_embeddings(input_descriptors_embedding).tolist()
    input_filters = data["filters"]
    mongo_filters = [{"rating": {"$gte": input_filters["Rating"]}}]
    gender_mapping = {"For Men": "men", "For Women": "women", "Unisex": "unisex"}
    if input_filters["Brand"]:
        mongo_filters.append({"brand": {"$in": input_filters["Brand"]}})
    if input_filters["Country of Origin"]:
        mongo_filters.append({"country": {"$in": input_filters["Country of Origin"]}})
    if input_filters["Exclude Notes/Accords"]:
        mongo_filters.append(
            {"descriptors": {"$not": {"$in": input_filters["Exclude Notes/Accords"]}}}
        )
    if input_filters["Gender"]:
        input_filters["Gender"] = [gender_mapping[x] for x in input_filters["Gender"]]
        mongo_filters.append({"gender": {"$in": input_filters["Gender"]}})
    if input_filters["PopularityRange"]:
        quintiles = [0.503, 0.544, 0.593, 0.658, 0.946]
        range = input_filters["PopularityRange"]
        filter = []
        for r in range:
            if r[0] == 0 and r[1] == (len(quintiles) - 1):
                break
            if r[0] == r[1]:
                quintile = quintiles[r[0]]
                if r[0] == 0:
                    filter.append({"popularity": {"$lte": quintile}})
                    continue
                if r[0] == (len(quintiles) - 1):
                    filter.append({"popularity": {"$gte": quintiles[r[0] - 1]}})
                    continue
                filter.append(
                    {"popularity": {"$gte": quintiles[r[0] - 1], "$lte": quintile}}
                )
                continue
            quintile = quintiles[r[1]]
            if r[0] == 0:

                filter.append({"popularity": {"$lte": quintile}})
                continue
            filter.append(
                {"popularity": {"$gte": quintiles[r[0] - 1], "$lte": quintile}}
            )

        obj = {"$or": filter}
        print(obj)
        mongo_filters.append(obj)

    results = frag_db["fragrances"].aggregate(
        [
            {
                "$vectorSearch": {
                    "index": "fragranceVectorSearch",
                    "path": "fragranceVector",
                    "queryVector": input_embedding,
                    "numCandidates": 1000,
                    "limit": 100,
                    "filter": {"$and": mongo_filters},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "gender": 1,
                    "country": 1,
                    "year": 1,
                    "brand": 1,
                    "topNotes": 1,
                    "midNotes": 1,
                    "baseNotes": 1,
                    "accords": 1,
                    "country": 1,
                    "rating": 1,
                    "popularity": 1,
                    "descriptors": 1,
                    "url": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]
    )

    # note coverage .55 limit .45 give half point
    results_list = list(results)

    for frag in results_list:
        # frag["coverage"] = 0.5 * coverage(
        #     input_descriptors_embedding,
        #     (frag["topNotes"] + frag["midNotes"] + frag["baseNotes"]),
        #     frag_db["notes"],
        # ) + 0.5 * coverage(
        #     input_descriptors_embedding,
        #     frag["accords"],
        #     frag_db["accords"],
        # )
        # frag["score"] = 0.2 * frag["coverage"] + 0.8 * frag["score"]
        del frag["topNotes"]
        del frag["midNotes"]
        del frag["baseNotes"]
        del frag["accords"]

    results_list.sort(key=lambda x: x["score"], reverse=True)

    return jsonify({"results": results_list})


@app.route("/api/v1/accords", methods=["GET"])
def get_accords():
    data = list(frag_db["accords"].find({}))
    return jsonify(data)


@app.route("/api/v1/brands", methods=["GET"])
def get_brands():
    data = list(frag_db["brands"].find({}))
    print(data)
    return jsonify(data)


@app.route("/api/v1/countries", methods=["GET"])
def get_countries():
    data = list(frag_db["countries"].find({}))
    return jsonify(data)


@app.route("/api/v1/notes", methods=["GET"])
def get_notes():
    data = list(frag_db["notes"].find({}))
    return jsonify(data)


@app.route("/api/v1/filters", methods=["GET"])
def get_filters():
    data = {}
    data["brands"] = [
        x["name"] for x in frag_db["brands"].find({}, {"_id": 0, "name": 1})
    ]
    data["countries"] = [
        x["name"] for x in frag_db["countries"].find({}, {"_id": 0, "name": 1})
    ]
    data["notes"] = [
        x["name"] for x in frag_db["notes"].find({}, {"_id": 0, "name": 1})
    ]
    data["accords"] = [
        x["name"] for x in frag_db["accords"].find({}, {"_id": 0, "name": 1})
    ]
    data["descriptors"] = list(set(data["notes"]) | set(data["accords"]))
    # add popularity
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
