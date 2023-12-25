import asyncio
import time

import config
from config import logger
from mongo_storage import MongoStorage
from parser import Parser
from rabbit_sender import RabbitSender


def setup_db_storage():
    mongo_storage = MongoStorage(mongo_uri=config.MONGO_URI,
                                 db_name=config.MONGO_DB_NAME,
                                 collection_name=config.MONGO_COLLECTION_NAME)
    return mongo_storage


def setup_message_broker():
    rabbit = RabbitSender(host=config.RABBITMQ_HOST,
                          port=config.RABBITMQ_PORT,
                          username=config.RABBITMQ_USERNAME,
                          password=config.RABBITMQ_PASSWORD,
                          queue_name=config.RABBITMQ_QUEUE_NAME)
    return rabbit


async def main():
    url = "https://www.benzinga.com/markets"
    try:
        rabbit = setup_message_broker()
        mongo_storage = setup_db_storage()

        parser = Parser(url=url,
                        message_broker=rabbit,
                        database_storage=mongo_storage)
        while True:
            await parser.run(delay_time=config.DELAY_TIME)

    except Exception as error:
        logger.error(f"Main failed with error: {error}")

if __name__ == "__main__":
    time.sleep(5)  # Wait for rabbit_container starting, if your rabbit not in docker, delete this
    asyncio.run(main())
