from fastapi import FastAPI
from app.api.routes import router
from app.database.db import engine, Base
from app.database import models

app = FastAPI(
    title="Custom Auth System",
    description="Custom authentication and authorization system with JWT",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)
app.include_router(router)
