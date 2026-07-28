from fastapi import FastAPI
from fastapi import Query
from typing import Optional
from app.services.search_service import build_query
from app.clients.mongo_client import query_collection

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/api/v1/search/")
def search(
    descriptors: list[str] = Query(
        ...,
        min_length=1,
        description="Notes and accords user wants to see in fragrance results.",
    ),
    brands: Optional[list[str]] = Query(None),
    rating: Optional[int] = Query(None),
    countries: Optional[list[str]] = Query(None),
    popularity: Optional[list[int]] = Query(None),
    excluded_descriptors: Optional[list[str]] = Query(..., min_length=1),
):
    print(
        query_collection(
            "fragrances",
            build_query(brands, rating, countries, popularity, excluded_descriptors),
        )
    )
    return False


@app.get("/api/v1/match/")
def match(
    fragrance: str = Query(...),
    brands: Optional[list[str]] = Query(None),
    rating: Optional[int] = Query(None),
    countries: Optional[list[str]] = Query(None),
    popularity: Optional[int] = Query(None),
    excluded_descriptors: Optional[list[str]] = Query(..., min_length=1),
):
    pass


if __name__ == "__main__":
    pass
