from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.v1.endpoints import tasks
from src.api.v1.endpoints.auth import router as auth_router
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield


app = FastAPI(title="Todo Backend API", version="1.0.0", lifespan=lifespan)

# Include API routes
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}