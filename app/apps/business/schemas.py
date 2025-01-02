from pydantic import BaseModel, model_validator
from ufaas_fastapi_business.schemas import BusinessSchema as BaseBusinessSchema

from server.config import Settings


class FieldConfig(BaseModel):
    mandatory: list[str] = []
    unique: list[str] = []


class BusinessSchema(BaseBusinessSchema):
    field_config: FieldConfig = FieldConfig()

    @model_validator(mode="before")
    def validate_domain(data: dict):
        business_name_domain = f"{data.get('name')}.{Settings.root_url}"
        if not data.get("domain"):
            data["domain"] = business_name_domain

        return data
