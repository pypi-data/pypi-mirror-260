from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from .exception.internal_exception import DatabaseInitializeFailureException, DatabaseConnectFailureException


class MongoDB:
    def __init__(self, connection_url: str, db_name: str):
        self.client = None
        self.connection_url = connection_url
        self.db_name = db_name

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.connection_url)
        except ServerSelectionTimeoutError:
            raise DatabaseInitializeFailureException()

    async def close(self):
        if self.client:
            self.client.close()

    def get_database(self):
        if not self.client:
            raise DatabaseConnectFailureException()
        return self.client[self.db_name]
