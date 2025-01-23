from apps.business.routes import router as business_router
from apps.profiles.routes import router as profile_router
from fastapi_mongo_base.core import app_factory

from . import config

app = app_factory.create_app(
    settings=config.Settings(),
    origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "https://pixiee.io",
        "https://pixy.ir",
    ],
    ufaas_handler=False,
)

app.include_router(business_router)
app.include_router(profile_router)
