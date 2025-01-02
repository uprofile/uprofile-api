import uuid

from fastapi_mongo_base.schemas import BusinessOwnedEntitySchema
from pydantic import BaseModel


class ProfileSchema(BusinessOwnedEntitySchema):
    def __init__(self, **data):
        super().__init__(**data)
        self.uid = self.user_id

    profile_data: dict = {}


class ProfileCreateSchema(BaseModel):
    user_id: uuid.UUID | None
    meta_data: dict | None = None
    profile_data: dict = {}


class ProfileUpdateSchema(BaseModel):
    meta_data: dict | None = None
    profile_data: dict = {}
