from fastapi_mongo_base.models import BusinessOwnedEntity

from .schemas import ProfileSchema


class Profile(ProfileSchema, BusinessOwnedEntity):
    class Settings:
        indexes = BusinessOwnedEntity.Settings.indexes
