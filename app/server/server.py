from apps.business.routes import router as business_router
from apps.profiles.routes import router as profile_router
from fastapi_mongo_base.core import app_factory

from . import config

app = app_factory.create_app(
    settings=config.Settings(),
    origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "https://cmp.liara.run",
        "https://app.pixiee.io",
        "https://pixiee.io",
        "https://pixy.ir",
        "https://stg.pixiee.io",
        "https://cmp-dev.liara.run",
        "https://pixiee.bot.inbeet.tech",
        "https://picsee.bot.inbeet.tech",
        "https://dashboard.pixiee.bot.inbeet.tech",
    ],
    ufaas_handler=False,
)

app.include_router(business_router)
app.include_router(profile_router)

