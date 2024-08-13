from pathlib import Path
import tomllib
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv()

with open(BASE_DIR / "pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)
    project_version = pyproject_data["tool"]["poetry"]["version"]
    project_name = pyproject_data["tool"]["poetry"]["name"]
    project_description = pyproject_data["tool"]["poetry"]["description"]
    project_author = pyproject_data["tool"]["poetry"]["authors"][0]


class Settings(BaseSettings):
    PROJECT_NAME: str = project_name
    PROJECT_VERSION: str = project_version
    PROJECT_DESCRIPTION: str = project_description
    PROJECT_AUTHOR: str = project_author

    DB_ECHO: bool = False
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google"
    JWT_ALGORITHM: list[str] = ["HS256", ]
    SECRET_KEY: str

    ALGORITHM: str = "RS256"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
