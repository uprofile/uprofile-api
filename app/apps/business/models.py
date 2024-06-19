from pydantic import BaseModel, model_validator

from apps.base.models import OwnedEntity
from apps.plugins.models import Plugin
from server.config import Settings


class FieldConfig(BaseModel):
    mandatory: list[str] = []
    unique: list[str] = []


class Business(OwnedEntity):
    name: str
    description: str | None = None
    domain: str
    field_config: FieldConfig
    plugins: list[Plugin] = []

    # class Settings:
    #     indexes = [
    #         {"keys": [("name", 1)], "unique": True},
    #         {"keys": [("domain", 1)], "unique": True},
    #     ]

    @classmethod
    async def get_by_origin(cls, origin: str):
        return await cls.find_one(cls.domain == origin)

    @model_validator(mode="before")
    def validate_domain(data: dict):
        business_name_domain = f"https://{data.get('name')}.{Settings.root_url}"
        if not data.get("domain"):
            data["domain"] = business_name_domain

        return data
