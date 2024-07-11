from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv()


class Settings(BaseSettings):
    db_echo: bool = False
    # db_echo: bool = True
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    ALGORITHM: str = "RS256"

    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
