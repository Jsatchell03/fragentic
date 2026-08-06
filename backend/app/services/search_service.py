from app.schemas.api_schemas import DescriptorQuery, FragranceQuery, VectorQuery
from app.services import embedding_service
from app.clients.mongo_client import execute_pipeline
from app.config import settings

NUM_CANDIDATES = settings.search.num_candidates
PAGE_SIZE = settings.search.page_size
VECTOR_SEARCH_LIMIT = settings.search.vector_search_limit


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


def search_by_descriptors(query: DescriptorQuery):
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
        "limit": VECTOR_SEARCH_LIMIT,
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
                "all_descriptors": 1,
                "vector_score": {"$meta": "vectorSearchScore"},
            }
        },
        {
            "$setWindowFields": {
                "sortBy": {"vector_score": -1},
                "output": {
                    "min_vector_score": {
                        "$min": "$vector_score",
                        "window": {"documents": ["unbounded", "unbounded"]},
                    },
                    "max_vector_score": {
                        "$max": "$vector_score",
                        "window": {"documents": ["unbounded", "unbounded"]},
                    },
                },
            }
        },
        {
            "$addFields": {
                "normalized_vector_score": {
                    "$cond": [
                        {"$eq": ["$max_vector_score", "$min_vector_score"]},
                        1,
                        {
                            "$divide": [
                                {"$subtract": ["$vector_score", "$min_vector_score"]},
                                {
                                    "$subtract": [
                                        "$max_vector_score",
                                        "$min_vector_score",
                                    ]
                                },
                            ]
                        },
                    ]
                }
            }
        },
        {
            "$addFields": {
                "keyword_intersection": {
                    "$setIntersection": ["$all_descriptors", query.descriptors]
                },
                "keyword_union": {"$setUnion": ["$all_descriptors", query.descriptors]},
            }
        },
        {
            "$addFields": {
                "jaccard_score": {
                    "$cond": [
                        {"$eq": [{"$size": "$keyword_union"}, 0]},
                        0,
                        {
                            "$divide": [
                                {"$size": "$keyword_intersection"},
                                {"$size": "$keyword_union"},
                            ]
                        },
                    ]
                }
            }
        },
        {
            "$addFields": {
                "score": {
                    "$add": [
                        {"$multiply": ["$normalized_vector_score", 0.75]},
                        {"$multiply": ["$jaccard_score", 0.25]},
                    ]
                }
            }
        },
        {"$sort": {"score": -1}},
        {"$limit": PAGE_SIZE},
        {
            "$project": {
                "min_vector_score": 0,
                "max_vector_score": 0,
                "keyword_intersection": 0,
                "keyword_union": 0,
                "jaccard_score": 0,
                "vector_score": 0,
                "normalized_vector_score": 0,
            }
        },
    ]

    results = list(execute_pipeline("fragrances", pipeline))

    return {"search_vector": search_vector, "fragrances": results}


def search_by_fragrance(query):
    pass


def search_by_vector(query):
    filter_component = build_filter_component(
        query.model_dump(exclude={"search_vector", "descriptors"})
    )
    vector_search_component = {
        "index": "fragrance_vector_index",
        "path": "fragrance_vector",
        "queryVector": query.search_vector,
        "numCandidates": NUM_CANDIDATES,
        "limit": VECTOR_SEARCH_LIMIT,
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
                "all_descriptors": 1,
                "vector_score": {"$meta": "vectorSearchScore"},
            }
        },
        {
            "$setWindowFields": {
                "sortBy": {"vector_score": -1},
                "output": {
                    "min_vector_score": {
                        "$min": "$vector_score",
                        "window": {"documents": ["unbounded", "unbounded"]},
                    },
                    "max_vector_score": {
                        "$max": "$vector_score",
                        "window": {"documents": ["unbounded", "unbounded"]},
                    },
                },
            }
        },
        {
            "$addFields": {
                "normalized_vector_score": {
                    "$cond": [
                        {"$eq": ["$max_vector_score", "$min_vector_score"]},
                        1,
                        {
                            "$divide": [
                                {"$subtract": ["$vector_score", "$min_vector_score"]},
                                {
                                    "$subtract": [
                                        "$max_vector_score",
                                        "$min_vector_score",
                                    ]
                                },
                            ]
                        },
                    ]
                }
            }
        },
        {
            "$addFields": {
                "keyword_intersection": {
                    "$setIntersection": ["$all_descriptors", query.descriptors]
                },
                "keyword_union": {"$setUnion": ["$all_descriptors", query.descriptors]},
            }
        },
        {
            "$addFields": {
                "jaccard_score": {
                    "$cond": [
                        {"$eq": [{"$size": "$keyword_union"}, 0]},
                        0,
                        {
                            "$divide": [
                                {"$size": "$keyword_intersection"},
                                {"$size": "$keyword_union"},
                            ]
                        },
                    ]
                }
            }
        },
        {
            "$addFields": {
                "score": {
                    "$add": [
                        {"$multiply": ["$normalized_vector_score", 0.75]},
                        {"$multiply": ["$jaccard_score", 0.25]},
                    ]
                }
            }
        },
        {"$sort": {"score": -1}},
        {"$limit": PAGE_SIZE},
        {
            "$project": {
                "min_vector_score": 0,
                "max_vector_score": 0,
                "keyword_intersection": 0,
                "keyword_union": 0,
                "jaccard_score": 0,
                "vector_score": 0,
                "normalized_vector_score": 0,
            }
        },
    ]

    results = list(execute_pipeline("fragrances", pipeline))

    return {"search_vector": query.search_vector, "fragrances": results}


if __name__ == "__main__":
    sample_query = DescriptorQuery(
        descriptors=["apple", "fresh", "sweet", "citrus", "vanilla", "lemon", "woody"],
        popularity=[4, 5],
    )
    print((search_by_descriptors(sample_query))["fragrances"])
