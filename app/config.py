from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Code Review Platform"
    app_version: str = "0.1.0"

    github_token: str | None = None
    github_webhook_secret: str | None = None
    github_api_url: str = "https://api.github.com"

    llm_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_timeout: float = 30.0
    llm_retries: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()