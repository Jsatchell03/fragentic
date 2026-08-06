from app.clients import mongo_client
from app.schemas.app_schemas import Descriptor
from app.schemas.db_schemas import DescriptorDoc, FragranceDoc

STORED_DESCRIPTOR_NAMES = set(
    descriptor["name"] for descriptor in mongo_client.get_all("descriptors")
)

STORED_FRAGRANCE_URLS = set(
    fragrance["fragrantica_url"] for fragrance in mongo_client.get_all("fragrances")
)


def find_descriptors(names):
    query = {"name": {"$in": names}}
    results = mongo_client.query_collection("descriptors", query)
    if results:
        return [
            Descriptor(name=doc["name"], list_vector=doc["vector"])
            for doc in list(results)
        ]
    return []


def upload_descriptors(descriptors: list[DescriptorDoc]):
    mongo_client.upload_many(
        "descriptors",
        [descriptor.model_dump(mode="json") for descriptor in descriptors],
    )


def upload_fragrances(fragrances: list[FragranceDoc]):
    mongo_client.upload_many(
        "fragrances", [fragrance.model_dump(mode="json") for fragrance in fragrances]
    )


def find_fragrance(id):
    pass


def vector_search_fragrances(vector, filters: dict):
    query = {}
    if filters["brands"]:
        query["brand"] = {"$in": filters["brands"]}
    if filters["rating"]:
        query["rating"] = {"$gte": filters["rating"]}
    if filters["countries"]:
        query["country"] = {"$in": filters["countries"]}
    if filters["popularity"]:
        query["popularity"] = {"$in": filters["popularity"]}
    if filters["excluded_descriptors"]:
        query["top_notes"] = {"$nin": filters["excluded_descriptors"]}
        query["mid_notes"] = {"$nin": filters["excluded_descriptors"]}
        query["base_notes"] = {"$nin": filters["excluded_descriptors"]}
        query["accords"] = {"$nin": filters["excluded_descriptors"]}
    return query
