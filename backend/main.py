from fastapi import FastAPI
from fastapi import Query
from typing import Annotated
from app.services.search_service import (
    search_by_descriptors,
    search_by_fragrance,
    search_by_vector,
)
from app.clients.mongo_client import query_collection
from app.schemas.api_schemas import (
    VectorQuery,
    DescriptorQuery,
    FragranceQuery,
    SearchResults,
    FragranceResponse,
)

app = FastAPI()


# @app.get("/api/v1/search/fragrance/{id}")
# def search(query: Annotated[FragranceQuery, Query()]) -> SearchResults:
#     search_results = search_by_descriptors(query)
#     return search_results


@app.get("/api/v1/search/descriptors")
def search_descriptors(query: Annotated[DescriptorQuery, Query()]) -> SearchResults:
    search_results = search_by_descriptors(query)

    return SearchResults(
        search_vector=search_results["search_vector"].tolist(),
        fragrances=[
            FragranceResponse(**fragrance) for fragrance in search_results["fragrances"]
        ],
    )


@app.get("/api/v1/search/vector")
def search_vector(query: Annotated[VectorQuery, Query()]) -> SearchResults:
    search_results = search_by_vector(query)
    return SearchResults(
        search_vector=search_results["search_vector"],
        fragrances=[
            FragranceResponse(**fragrance) for fragrance in search_results["fragrances"]
        ],
    )


if __name__ == "__main__":
    pass
