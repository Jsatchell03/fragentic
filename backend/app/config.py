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


class ETLConfig(BaseModel):
    cache_max_size: int
    note_weight: float
    accord_weight: float
    top_note_weight: float
    mid_note_weight: float
    base_note_weight: float
    batch_size: int


class AppSettings(BaseSettings):
    model_config = {"yaml_file": BASE_DIR / "config.yaml"}
    openai: OpenAIConfig
    etl: ETLConfig

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
