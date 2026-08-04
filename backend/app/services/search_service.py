from app.services import db_service
from app.schemas.requests_schemas import SearchQuery
from app.services import embedding_service


def search_by_descriptors(query: SearchQuery):
    hits, misses = embedding_service.get_descriptors(query.descriptors)
    cached_vectors = [descriptor["vector"] for descriptor in hits]
    if len(misses) > 0:
        stored_descriptors = db_service.find_descriptors(misses)
        stored_descriptor_names = [
            descriptor["name"] for descriptor in stored_descriptors
        ]

        vectors = cached_vectors + [
            descriptor["vector"] for descriptor in db_service.find_descriptors(misses)
        ]

        if len(stored_descriptors) < len(misses):
            new_descriptors = []
            for descriptor in misses:
                if descriptor not in stored_descriptor_names:
                    new_descriptors.append(descriptor)
            vectors += embedding_service.get_many_embeddings(new_descriptors).tolist()
    else:
        vectors = cached_vectors

    search_vector = embedding_service.avg_vectors(vectors)
    filters = query.model_dump(exclude={"descriptors"})
    search_results = db_service.vector_search_fragrances(search_vector, filters)
    return search_results


def search_by_fragrance(query):
    pass
