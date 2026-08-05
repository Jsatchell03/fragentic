from app.services import db_service
from app.schemas.requests_schemas import SearchQuery
from app.services import embedding_service
from app.clients.mongo_client import execute_pipeline
from app.config import settings

NUM_CANDIDATES = settings.search.num_candidates
PAGE_SIZE = settings.search.page_size


def build_filter_component(filters):
    res = []
    if filters["rating"]:
        res.append({"rating": {"$gte": filters["rating"]}})
    if filters["brands"]:
        res.append({"brand": {"$in": filters["brands"]}})

    if filters["countries"]:
        res.append({"country": {"$in": filters["countries"]}})
    if filters["popularity"]:
        res.append({"popularity": {"$in": filters["popularity"]}})
    if filters["excluded_descriptors"]:
        res.append({"all_descriptors": {"$nin": filters["excluded_descriptors"]}})

    if len(res) == 0:
        return None

    return {"$and": res}


def search_by_descriptors(query: SearchQuery):
    search_vector = embedding_service.l2_normalize(
        embedding_service.avg_vectors(
            [
                descriptor.np_vector
                for descriptor in embedding_service.embed_descriptors(query.descriptors)
            ]
        )
    )
    filter_component = build_filter_component(query.model_dump(exclude={"descriptors"}))
    vector_search_component = {
        "index": "fragrance_vector_index",
        "path": "fragrance_vector",
        "queryVector": search_vector.tolist(),
        "numCandidates": NUM_CANDIDATES,
        "limit": PAGE_SIZE,
    }
    if filter_component:
        vector_search_component["filter"] = filter_component
    pipeline = [
        {"$vectorSearch": vector_search_component},
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "top_notes": 1,
                "mid_notes": 1,
                "base_notes": 1,
                "accords": 1,
                "brand": 1,
                "rating": 1,
                "gender": 1,
                "score": {"$meta": "vectorSearchScore"},  # Retrieve the match score
            }
        },
    ]

    results = execute_pipeline("fragrances", pipeline)

    return results


def build_keyword_pipeline(search_descriptors):
    jaccard_stages = [
        {
            "$addFields": {
                "matched_notes": {
                    "$setIntersection": ["$all_descriptors", search_descriptors]
                }
            }
        },
        {
            "$addFields": {
                "matched_count": {"$size": "$matched_notes"},
                "union_count": {
                    "$size": {"$setUnion": ["$all_descriptors", search_descriptors]}
                },
            }
        },
        {
            "$addFields": {
                "keyword_score": {
                    "$cond": [
                        {"$eq": ["$union_count", 0]},
                        0,
                        {"$divide": ["$matched_count", "$union_count"]},
                    ]
                }
            }
        },
    ]


def build_vector_pipeline(search_vector):
    pass


def search_by_fragrance(query):
    pass


if __name__ == "__main__":
    sample_query = SearchQuery(
        descriptors=["green apple, citrus, sweet, fresh"],
        brands=["Versace"],
        popularity=[4, 5],
    )

    print(list(search_by_descriptors(sample_query)))
