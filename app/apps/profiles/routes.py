from usso.fastapi import jwt_access_security

from apps.business.routes import AbstractBusinessBaseRouter

from .models import Profile


class ProfileRouter(AbstractBusinessBaseRouter[Profile]):
    def __init__(self):
        super().__init__(
            model=Profile,
            user_dependency=jwt_access_security,
            resource_name="/profiles",
        )


router = ProfileRouter().router
