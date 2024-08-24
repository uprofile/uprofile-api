from typing import TypeVar

from apps.base.models import BusinessEntity, BusinessOwnedEntity
from apps.business.models import Business
from core.exceptions import BaseHTTPException
from fastapi import Request

from .middlewares import get_business

T = TypeVar("T", bound=BusinessEntity)
OT = TypeVar("OT", bound=BusinessOwnedEntity)


def create_dto_business(cls: OT):

    async def dto(
        request: Request,
        user=None,
        **kwargs
    ):
        business: Business = await get_business(request)
        form_data = await request.json()
        if form_data.get("user_id"):
            if user.uid == business.user_id:
                return cls(**form_data, business_id=business.uid)

        if user:
            form_data["user_id"] = user.uid
        return cls(**form_data, business_id=business.uid)

    return dto


def update_dto_business(cls: OT):

    async def dto(
        request: Request,
        user=None,
        **kwargs
    ):
        business: Business = await get_business(request)
        uid = request.path_params["uid"]
        form_data = await request.json()
        kwargs = {}
        if user:
            kwargs["user_id"] = user.uid
        item = await cls.get_item(uid, business_id=business.uid, **kwargs)

        if not item:
            raise BaseHTTPException(
                status_code=404,
                error="item_not_found",
                message="Item not found",
            )

        item_data = item.model_dump() | form_data

        return cls(**item_data)

    return dto
