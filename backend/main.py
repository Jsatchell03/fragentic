from fastapi import FastAPI
from fastapi import Query
from typing import Annotated
from app.services.search_service import search_by_descriptors, search_by_fragrance
from app.clients.mongo_client import query_collection
from app.schemas.requests_schemas import SearchQuery, MatchQuery

app = FastAPI()


@app.get("/api/v1/search/")
def search(query: Annotated[SearchQuery, Query()]):
    return search_by_descriptors(query)


@app.get("/api/v1/match/")
def match(query: Annotated[MatchQuery, Query()]):
    return search_by_fragrance(query)


if __name__ == "__main__":
    pass
