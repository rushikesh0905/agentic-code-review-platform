from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Code Review Platform"
    app_version: str = "0.1.0"

    github_token: str | None = None
    github_webhook_secret: str | None = None
    github_api_url: str = "https://api.github.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()