from typing import TypeVar

from fastapi import Depends, Request

from apps.base.models import BusinessEntity, BusinessOwnedEntity
from apps.business.models import Business
from core.exceptions import BaseHTTPException

from .middlewares import get_business

T = TypeVar("T", bound=BusinessEntity)
OT = TypeVar("OT", bound=BusinessOwnedEntity)


def create_dto_business(cls: OT):

    async def dto(
        request: Request,
        user=None,
        business: Business = Depends(get_business),
        **kwargs
    ):
        form_data = await request.json()
        if user:
            form_data["user_id"] = user.uid
        return cls(**form_data, business_id=business.uid)

    return dto


def update_dto_business(cls: OT):

    async def dto(
        request: Request,
        user=None,
        business: Business = Depends(get_business),
        **kwargs
    ):
        uid = request.path_params["uid"]
        form_data = await request.json()
        kwargs = {}
        if user:
            kwargs["user"] = user
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
