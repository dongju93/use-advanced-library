from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


def check_mongodb_connection() -> tuple[bool, str]:
    uri = "mongodb://localhost:27017"
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        client.admin.command("ping")

        return True, "MongoDB 서버에 정상적으로 연결되었습니다."

    except ConnectionFailure as e:
        return False, f"MongoDB 서버 연결 실패: {str(e)}"
    except OperationFailure as e:
        return False, f"MongoDB 인증 실패: {str(e)}"
    except Exception as e:
        return False, f"예상치 못한 오류 발생: {str(e)}"

    finally:
        if "client" in locals():
            client.close()
