from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message": "Vantora API is running"}