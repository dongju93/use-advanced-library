from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db: str


class Settings(BaseSettings):
    database: DatabaseConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # TOML 설정 소스만 반환
        return (TomlConfigSettingsSource(settings_cls, toml_file="app/.internal.toml"),)
