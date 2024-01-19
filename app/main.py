from fastapi import FastAPI

app = FastAPI(title="Delivery Fee Calculator API")


@app.get("/")
def hello_world():
    return {"Hello": "World"}
