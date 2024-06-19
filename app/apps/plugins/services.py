import aiohttp

from .models import Plugin


async def check(application: Plugin, profile: dict):
    if not all([profile.get(field) for field in application.target_fields]):
        return False
    target_fields = {field: profile.get(field) for field in application.target_fields}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            application.url,
            json=target_fields,
            headers={"Authorization": application.api_key},
        ) as response:
            return response.status == 200
