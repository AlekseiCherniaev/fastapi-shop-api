from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config.config import settings
from app.config.logger import logger
from app.adapters.routers.auth import router as auth_router
from app.adapters.routers.users import router as users_router
from app.adapters.routers.users_crud import router as users_crud_router
# from app.adapters.routers.auth_google import router as auth_google_router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Starting FastAPI app")
    yield
    logger.info("Shutting down FastAPI app")


app = FastAPI(lifespan=lifespan,
              version=settings.PROJECT_VERSION,
              title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              )

SECRET_KEY = settings.SECRET_KEY
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(users_crud_router)
# app.include_router(auth_google_router)


@app.get("/healthcheck")
def read_root():
    return {"status": "ok"}
