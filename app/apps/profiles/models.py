from apps.base.models import BusinessOwnedEntity


class Profile(BusinessOwnedEntity):
    data: dict = {}
