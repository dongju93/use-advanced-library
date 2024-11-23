from contextlib import asynccontextmanager

import uvloop
from fastapi import Body, FastAPI, Path, Query

from .database.model.table import User
from .database.model.types import MongoMoviesUpdate
from .database.mongo import MongoDB, Motor
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


@app.get("/mongo/health")
async def mongo_connection_is_up():
    logger.info("Checking MongoDB connection")
    mongo = MongoDB()
    is_up, message = mongo.check_mongodb_connection()
    return {"is_up": is_up, "message": message}


@app.post("/mongo")
async def mongo_data_insert():
    logger.info("Inserting data into MongoDB")
    mongo = MongoDB()
    mongo.insert_movie_document()
    return {"message": "Data inserted successfully"}


@app.get("/mongo/{doc_id}")
async def mongo_data_search(doc_id: int = Path(...)):
    logger.info(f"Searching data from MongoDB with doc_id: {doc_id}")
    mongo = MongoDB()
    data = mongo.search_movie_document(doc_id)
    return data


@app.patch("/mongo/{doc_id}")
async def mongo_data_update(
    doc_id: int = Path(...), update_data: MongoMoviesUpdate = Body(...)
):
    logger.info(f"Updating data from MongoDB with doc_id: {doc_id}")
    mongo = MongoDB()
    modified_count = mongo.update_movie(doc_id, update_data)
    return {"modified_count": modified_count}


@app.get("/motor/health")
async def mongo_connection_is_up_motor():
    logger.info("Checking MongoDB connection")
    is_up, message = await Motor().check_motor_connection()
    return {"is_up": is_up, "message": message}
