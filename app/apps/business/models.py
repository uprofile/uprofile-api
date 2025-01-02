from fastapi_mongo_base.models import OwnedEntity
from ufaas_fastapi_business.schemas import BusinessSchema

from .schemas import BusinessSchema


class Business(BusinessSchema, OwnedEntity):
    class Settings:
        indexes = OwnedEntity.Settings.indexes

    @classmethod
    async def get_by_origin(cls, origin: str):
        return await cls.find_one(cls.domain == origin)
