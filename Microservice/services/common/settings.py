from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str


class MinioSettings(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    region: str = "eu-central-1"
    bucket_imagery: str = "imagery"
    bucket_heatmaps: str = "heatmaps"
    bucket_reports: str = "reports"


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "env.example"), extra="ignore")

    service_name: str = Field(default="service")
    gateway_port: int = Field(default=8080, alias="GATEWAY_PORT")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    imagery_service_url: str = Field(
        default="http://imagery-service:8001", alias="IMAGERY_SERVICE_URL"
    )
    analysis_service_url: str = Field(
        default="http://analysis-service:8002", alias="ANALYSIS_SERVICE_URL"
    )
    report_service_url: str = Field(
        default="http://report-service:8003", alias="REPORT_SERVICE_URL"
    )

    imagery_db: DatabaseSettings = Field(
        default_factory=lambda: DatabaseSettings(
            host="postgres-imagery",
            port=5432,
            name="imagery_db",
            user="imagery_user",
            password="imagery_pass",
        )
    )
    analysis_db: DatabaseSettings = Field(
        default_factory=lambda: DatabaseSettings(
            host="postgres-analysis",
            port=5432,
            name="analysis_db",
            user="analysis_user",
            password="analysis_pass",
        )
    )
    report_db: DatabaseSettings = Field(
        default_factory=lambda: DatabaseSettings(
            host="postgres-report",
            port=5432,
            name="report_db",
            user="report_user",
            password="report_pass",
        )
    )
    minio: MinioSettings = Field(
        default_factory=lambda: MinioSettings(
            endpoint="http://minio:9000",
            access_key="localminio",
            secret_key="localminio123",
        )
    )


@lru_cache
def get_settings() -> ServiceSettings:
    return ServiceSettings()

