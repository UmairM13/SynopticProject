from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommendation_engine.api.models.database import Base, engine
from recommendation_engine.api.routes.user_routes import router as user_router
from recommendation_engine.api.routes.recommendations_routes import router as recommendations
from recommendation_engine.api.routes.analytics_routes import router as analytics
from recommendation_engine.api.routes.destination_routes import router as destinations


app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite frontend
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can be ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods like GET, POST, etc.
    allow_headers=["*"],  # Allow all headers including X-Authorization
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/travel/api/users", tags=["Users"])
app.include_router(recommendations, prefix="/travel/api/recommendations", tags=["Recommendations"])
app.include_router(analytics, prefix="/travel/api/analytics", tags=["Analytics"])
app.include_router(destinations, prefix="/travel/api/destinations", tags=["Destinations"])


@app.get("/travel/api/")
def root():
    return {"message": "Welcome to the Travel Recommendation Engine API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)