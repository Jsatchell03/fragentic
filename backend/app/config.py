from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class OpenAIConfig(BaseModel):
    model: str
    dimensions: int


class RedisConfig(BaseModel):
    key_prefix: str


class ETLConfig(BaseModel):
    note_weight: float
    accord_weight: float
    accord_decay: float
    top_notes_weight: float
    mid_notes_weight: float
    base_notes_weight: float
    batch_size: int


class AppSettings(BaseSettings):
    model_config = {"yaml_file": BASE_DIR / "config.yaml"}
    openai: OpenAIConfig
    etl: ETLConfig
    redis: RedisConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


settings = AppSettings()
