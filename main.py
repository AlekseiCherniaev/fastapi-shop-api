from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.config.logger import logger


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Starting FastAPI app")
    yield
    logger.info("Shutting down FastAPI app")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
