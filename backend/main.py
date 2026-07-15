from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.post("/api/v1/search")
# def search():
#     pass


# @app.get("/api/v1/constants")
# def get_constants():
#     pass


if __name__ == "__main__":
    pass
