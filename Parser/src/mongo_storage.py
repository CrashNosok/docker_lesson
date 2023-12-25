from config import logger
from Interfaces import DatabaseStorage
from motor.motor_asyncio import AsyncIOMotorClient


class MongoStorage(DatabaseStorage):
    def __init__(self, mongo_uri, db_name, collection_name):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name

    async def connect(self):
        client = AsyncIOMotorClient(self.mongo_uri)
        db = client.get_database(self.db_name)
        return db

    async def save(self, news_entry):
        try:
            db = await self.connect()
            collection = db.get_collection(self.collection_name)
            await collection.insert_one(news_entry)
            logger.info("News saved")

        except Exception as error:
            logger.error(f"Can`t save news to mongo with error: {error}")

    async def find_news(self, reference):
        try:
            db = await self.connect()
            collection = db.get_collection(self.collection_name)
            return await collection.count_documents({"reference": reference}) > 0

        except Exception as error:
            logger.error(f"Can`t check collection for news existing: {error}")
