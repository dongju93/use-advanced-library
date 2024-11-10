from contextlib import asynccontextmanager

import uvloop
from fastapi import Body, FastAPI, Query

from .database.model.table import User
from .database.mongo import check_mongodb_connection
from .database.query import create_user_row, get_user_row
from .logger import get_logger

uvloop.install()

logger = get_logger("api-router")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting the application")
    yield
    logger.info("Shutting down the application")


app = FastAPI(lifespan=lifespan)


@app.post("/user")
async def create_user(user: User = Body(...)):
    data = await create_user_row(user)
    return data


@app.get("/user")
async def get_user(user_idx: int = Query(...)):
    logger.info(f"Getting user data with user_idx: {user_idx}")
    data = await get_user_row(user_idx)
    logger.info(f"Get user data complete with user_idx: {user_idx}")
    return data


@app.get("/mongo")
async def mongo_connection_is_up():
    logger.info("Checking MongoDB connection")
    is_up, message = check_mongodb_connection()
    return {"is_up": is_up, "message": message}
