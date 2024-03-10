from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Type

from pydantic_settings import (BaseSettings, PydanticBaseSettingsSource,
                               SettingsConfigDict)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env.dev', '.env.prod', '.env'), env_file_encoding='utf-8')

    share_dmhy_org_tarcker_config_path: str = "storage/share_dmhy_org_tracker/config.json"
    bangumi_data_dir: str = "storage/bangumi"
