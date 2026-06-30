from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AION Backend Running"}