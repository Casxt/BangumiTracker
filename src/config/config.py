from pydantic_settings import (BaseSettings,
                               SettingsConfigDict)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env.dev', '.env.prod', '.env'), env_file_encoding='utf-8')

    share_dmhy_org_tarcker_config_path: str = "storage/tracker/share_dmhy_org.json"
    bangumi_data_dir: str = "storage/bangumi"
