from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.models import Task, User
from app.core.database import engine, Base
from app.api.router import auth_router, user_router , task_router, category_router  
from app.api.router import router
app = FastAPI(title="Todo List", version="1.0.0", description="FastAPI Todo List API")
app.mount("/media", StaticFiles(directory="media"), name="media")


Base.metadata.create_all(engine)

app.include_router(router, prefix="/api")

app.include_router(task_router.router)
app.include_router(category_router.router)

app.include_router(auth_router.router)
app.include_router(user_router.router)