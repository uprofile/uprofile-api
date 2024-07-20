from apps.business.handlers import create_dto_business
from apps.business.middlewares import get_business
from apps.business.models import Business
from apps.business.routes import AbstractBusinessBaseRouter
from fastapi import Depends, Request, APIRouter
from server.config import Settings
from usso.fastapi import jwt_access_security

from core.exceptions import BaseHTTPException

from .models import Profile


class ProfileRouter(AbstractBusinessBaseRouter[Profile]):

    def __init__(    self):
        self.model = Profile
        self.user_dependency = jwt_access_security
        tags = [self.model.__name__]
        self.router = APIRouter(prefix='/profiles', tags=tags)

        self.router.add_api_route(
            "/",
            self.list_items,
            methods=["GET"],
            response_model=list[self.model],
        )
        self.router.add_api_route(
            "/{uid:uuid}",
            self.retrieve_item,
            methods=["GET"],
            response_model=self.model,
        )
        self.router.add_api_route(
            "/",
            self.create_item,
            methods=["POST"],
            response_model=self.model,
            status_code=201,
        )
        self.router.add_api_route(
            "/{uid:uuid}",
            self.update_item,
            methods=["PATCH"],
            response_model=self.model,
        )
        self.router.add_api_route(
            "/{uid:uuid}",
            self.delete_item,
            methods=["DELETE"],
            response_model=self.model,
        )

    # def __init__(self):
    #     super().__init__(
    #         model=Profile,
    #         user_dependency=jwt_access_security,
    #         resource_name="/profiles",
    #     )

    async def list_items(
        self,
        request: Request,
        offset: int = 0,
        limit: int = 10,
        business: Business = Depends(get_business),
    ):
        user = await self.get_user(request)
        limit = max(1, min(limit, Settings.page_max_limit))

        items_query = (
            self.model.get_query(
                business_id=business.uid,
                user_id=None if business.user_id == user.uid else user.uid,
            )
            .sort("-created_at")
            .skip(offset)
            .limit(limit)
        )
        items = await items_query.to_list()
        return items

    async def retrieve_item(
        self,
        request: Request,
        uid,
        business: Business = Depends(get_business),
    ):
        user = await self.get_user(request)
        item = await self.model.get_item(
            uid,
            business_id=business.uid,
            user_id=None if business.user_id == user.uid else user.uid,
        )
        if item is None:
            raise BaseHTTPException(
                status_code=404,
                error="item_not_found",
                message=f"{self.model.__name__.capitalize()} not found",
            )
        return item

    async def create_item(self, request: Request):
        user = await self.get_user(request)
        item: Profile = await create_dto_business(self.model)(request, user)
        item.uid = item.user_id

        await item.save()
        return item


router = ProfileRouter().router
