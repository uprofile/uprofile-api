"""FastAPI server configuration."""

from pathlib import Path

import dotenv
from ufaas_fastapi_business.core.config import Settings as BaseSettings

dotenv.load_dotenv()


class Settings(BaseSettings):
    """Server config settings."""

    base_dir: Path = Path(__file__).resolve().parent.parent
