from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, users, articles, admin,digest
from app.admin.settings import admin
from starlette.middleware.sessions import SessionMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My App")

app.add_middleware(SessionMiddleware, secret_key="super-secret-key")
# Routers
app.include_router(auth.router)
app.include_router(users.router)

app.include_router(articles.router)
app.include_router(digest.router)
admin.mount_to(app)

