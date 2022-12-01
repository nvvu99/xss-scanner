from os import getenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from database.models import Request


async def init_db():
    host = getenv("MONGO_DB_HOST", "localhost")
    port = int(getenv("MONGO_DB_PORT", 27017))
    username = getenv("MONGO_DB_USER")
    password = getenv("MONGO_DB_PASSWORD")
    db_name = getenv("MONGO_DB_NAME")
    client = AsyncIOMotorClient(host, port, username=username, password=password)

    await init_beanie(database=client.get_database(db_name), document_models=[Request])
