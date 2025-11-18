from functools import lru_cache
from urllib.parse import urlparse

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    region: str = "eu-central-1"
    bucket_imagery: str = "imagery"
    bucket_heatmaps: str = "heatmaps"
    bucket_reports: str = "reports"

    @property
    def secure(self) -> bool:
        return self.endpoint.startswith("https://")

    @property
    def host(self) -> str:
        parsed = urlparse(self.endpoint if "://" in self.endpoint else f"http://{self.endpoint}")
        return parsed.netloc or parsed.path


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "env.example"), extra="ignore")

    service_name: str = Field(default="service", alias="SERVICE_NAME")
    gateway_port: int = Field(default=8080, alias="GATEWAY_PORT")

    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    broker_url: str = Field(default="redis://redis:6379/1", alias="BROKER_URL")
    result_url: str = Field(default="redis://redis:6379/2", alias="RESULT_URL")

    imagery_service_url: str = Field(
        default="http://imagery-service:8001", alias="IMAGERY_SERVICE_URL"
    )
    analysis_service_url: str = Field(
        default="http://analysis-service:8002", alias="ANALYSIS_SERVICE_URL"
    )
    report_service_url: str = Field(
        default="http://report-service:8003", alias="REPORT_SERVICE_URL"
    )

    minio_endpoint: str = Field(default="http://minio:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="localminio", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="localminio123", alias="MINIO_SECRET_KEY")
    minio_region: str = Field(default="eu-central-1", alias="MINIO_REGION")
    minio_bucket_imagery: str = Field(
        default="imagery", alias="MINIO_BUCKET_IMAGERY"
    )
    minio_bucket_heatmaps: str = Field(
        default="heatmaps", alias="MINIO_BUCKET_HEATMAPS"
    )
    minio_bucket_reports: str = Field(
        default="reports", alias="MINIO_BUCKET_REPORTS"
    )

    @property
    def minio(self) -> MinioSettings:
        endpoint = (
            self.minio_endpoint
            if "://" in self.minio_endpoint
            else f"http://{self.minio_endpoint}"
        )
        return MinioSettings(
            endpoint=endpoint,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            region=self.minio_region,
            bucket_imagery=self.minio_bucket_imagery,
            bucket_heatmaps=self.minio_bucket_heatmaps,
            bucket_reports=self.minio_bucket_reports,
        )


@lru_cache
def get_settings() -> ServiceSettings:
    return ServiceSettings()

