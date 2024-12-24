import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import asdict

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from app.utils.func_profiler import profile_performance

from .model.types import MongoMoviesUpdate


class MongoDB:
    @profile_performance()
    def check_mongodb_connection(self) -> tuple[bool, str]:
        try:
            with self._mongo_conn as mongo_client:
                mongo_client.admin.command("ping")

                return True, "MongoDB 서버에 정상적으로 연결되었습니다."

        except ConnectionFailure as e:
            return False, f"MongoDB 서버 연결 실패: {str(e)}"
        except OperationFailure as e:
            return False, f"MongoDB 인증 실패: {str(e)}"
        except Exception as e:
            return False, f"예상치 못한 오류 발생: {str(e)}"

    @profile_performance()
    def insert_movie_document(self):
        loaded_data = json.load(open("app/database/sample.json"))
        only_data_part = loaded_data["data"]["movies"]

        with self._mongo_conn as mongo_client:
            db = mongo_client["moviedb"]
            collection = db["movies"]
            result = collection.insert_many(only_data_part)
            print(f"삽입된 문서 수: {len(result.inserted_ids)}")
            print("삽입된 문서 ID들:", result.inserted_ids)

    @profile_performance()
    def search_movie_document(self, doc_id: int):
        with self._mongo_conn as mongo_client:
            db = mongo_client["moviedb"]
            collection = db["movies"]
            movie = collection.find_one({"id": doc_id})
            if movie:
                movie["_id"] = str(movie["_id"])
            return movie

    @profile_performance()
    def update_movie(self, movie_id: int, update_data: MongoMoviesUpdate):
        with self._mongo_conn as mongo_client:
            db = mongo_client["moviedb"]
            collection = db["movies"]
            result = collection.update_one(
                {"id": movie_id}, {"$set": asdict(update_data)}
            )
            return result.modified_count

    @property
    def _mongo_conn(self) -> MongoClient:
        uri = "mongodb://dongju:password@localhost:27017"
        return MongoClient(uri, serverSelectionTimeoutMS=5000)


class Motor:
    @profile_performance()
    async def check_motor_connection(self) -> tuple[bool, str]:
        try:
            async with self._motor_conn() as motor_client:
                await motor_client.admin.command("ping")

                return True, "MongoDB 서버에 정상적으로 연결되었습니다."

        except ConnectionFailure as e:
            return False, f"MongoDB 서버 연결 실패: {str(e)}"
        except OperationFailure as e:
            return False, f"MongoDB 인증 실패: {str(e)}"
        except Exception as e:
            return False, f"예상치 못한 오류 발생: {str(e)}"

    @profile_performance()
    @asynccontextmanager
    async def _motor_conn(
        self,
    ) -> AsyncGenerator[AsyncIOMotorClient, None]:
        uri = "mongodb://dongju:password@localhost:27017/?compressors=zstd"
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        try:
            yield client
        finally:
            client.close()
