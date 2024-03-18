from fastapi import FastAPI

app = FastApi()

@app.get("/")
def root():
    return {"Hello": "World"}