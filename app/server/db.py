from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis as RedisSync
from redis.asyncio.client import Redis

from apps.business.models import Business
from apps.plugins.models import Plugin
from apps.profiles.models import Profile

from .config import Settings

redis_sync: RedisSync = RedisSync.from_url(Settings.redis_uri)
redis: Redis = Redis.from_url(Settings.redis_uri)


async def init_db():
    client = AsyncIOMotorClient(Settings.mongo_uri)
    db = client.get_database(Settings.project_name)
    await init_beanie(
        database=db,
        document_models=[Business, Profile, Plugin],
    )
    return db
