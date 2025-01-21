import logging
import uuid
from datetime import datetime

from apps.business.middlewares import authorization_middleware
from fastapi import Query, Request
from fastapi_mongo_base.core.exceptions import BaseHTTPException
from server.config import Settings

# import routes import AbstractAuthRouter
from ufaas_fastapi_business.routes import AbstractAuthRouter
from usso.fastapi import jwt_access_security

from .models import Profile
from .schemas import ProfileCreateSchema, ProfileSchema, ProfileUpdateSchema


class ProfileRouter(AbstractAuthRouter[Profile, ProfileSchema]):

    def __init__(self):
        super().__init__(
            model=Profile, schema=ProfileSchema, user_dependency=jwt_access_security
        )

    async def get_auth(self, request: Request):
        return await authorization_middleware(request)

    async def list_items(
        self,
        request: Request,
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=0, le=Settings.page_max_limit),
        created_at_from: datetime | None = None,
        created_at_to: datetime | None = None,
        user_id: uuid.UUID | None = None,
    ):
        return await super().list_items(
            request, offset, limit, created_at_from, created_at_to
        )

    async def retrieve_item(self, request: Request, uid: uuid.UUID):
        auth = await self.get_auth(request)
        # item = await self.get_item(
        item = await Profile.find_one({"uid": uid, "business_name": auth.business.name})
        logging.info(f"{uid} {item} {auth.business.name}")
        if item is None:
            raise BaseHTTPException(
                status_code=404,
                error="item_not_found",
                message=f"{self.model.__name__.capitalize()} not found",
            )

        return item

    async def create_item(self, request: Request, profile: ProfileCreateSchema):
        auth = await self.get_auth(request)
        profile.user_id = auth.user_id
        item = self.model(business_name=auth.business.name, **profile.model_dump())
        # if auth.issuer_type == "User":
        item.uid = uuid.UUID(auth.user_id) if isinstance(auth.user_id, str) else auth.user_id
        await item.save()
        return self.create_response_schema(**item.model_dump())

    async def update_item(
        self, request: Request, uid: uuid.UUID, profile: ProfileUpdateSchema
    ):
        return await super().update_item(request, uid, profile.model_dump())


router = ProfileRouter().router
