from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
from app.api.router import router

app = FastAPI(title="Todo List", version="1.0.0", description="FastAPI Todo List API")
app.mount("/media", StaticFiles(directory="media"), name="media")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app.include_router(router, prefix="/api")
