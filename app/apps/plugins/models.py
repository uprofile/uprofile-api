from fastapi_mongo_base.models import OwnedEntity


class Plugin(OwnedEntity):
    name: str
    url: str
    api_key: str
    target_fields: list[str] = []
