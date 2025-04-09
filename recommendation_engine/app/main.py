from fastapi import FastAPI
from models.database import Base, engine
from routes.user_routes import router as user_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/travel/api")


@app.get("/")
def root():
    return {"message": "Welcome to the Travel Recommendation Engine API!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)