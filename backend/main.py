from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/api/v1/results/{result_hash}")
def search():
    pass


if __name__ == "__main__":
    pass
