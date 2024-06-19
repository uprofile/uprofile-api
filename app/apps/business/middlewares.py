from fastapi import Request

from apps.business.models import Business
from core.exceptions import BaseHTTPException


async def get_business(request: Request):
    business = await Business.get_by_origin(request.url.hostname)
    if not business:
        raise BaseHTTPException(404, "business_not_found", "business not found")
    return business
