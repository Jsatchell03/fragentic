from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from app.services.search_service import (
    search_by_descriptors,
    search_by_fragrance,
    search_by_vector,
)
from app.clients import mongo_client
from app.services import mongo_service
from app.schemas.api_schemas import (
    VectorQuery,
    DescriptorQuery,
    FragranceQuery,
    SearchResults,
    FragranceResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    names = await mongo_client.query_collection("descriptors", {}, {"name": 1, "_id": 0})
    mongo_service.STORED_DESCRIPTOR_NAMES = {d["name"] for d in (names or [])}
    urls = await mongo_client.query_collection("fragrances", {}, {"fragrantica_url": 1, "_id": 0})
    mongo_service.STORED_FRAGRANCE_URLS = {f["fragrantica_url"] for f in (urls or [])}
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/search/descriptors")
async def search_descriptors(query: Annotated[DescriptorQuery, Query()]) -> SearchResults:
    search_results = await search_by_descriptors(query)

    return SearchResults(
        search_vector=search_results["search_vector"].tolist(),
        fragrances=[
            FragranceResponse.model_validate(fragrance) for fragrance in search_results["fragrances"]
        ],
    )


@app.post("/api/v1/search/vector")
async def search_vector(query: VectorQuery) -> SearchResults:
    search_results = await search_by_vector(query)
    return SearchResults(
        search_vector=search_results["search_vector"],
        fragrances=[
            FragranceResponse.model_validate(fragrance) for fragrance in search_results["fragrances"]
        ],
    )


if __name__ == "__main__":
    pass
