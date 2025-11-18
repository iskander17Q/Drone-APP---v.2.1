import json
from datetime import datetime
from io import BytesIO
from typing import Any, Dict

from celery import Celery
from loguru import logger
from minio import Minio
from redis import Redis

from services.common.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "report_worker",
    broker=settings.broker_url,
    backend=settings.result_url,
)

redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
minio_cfg = settings.minio
minio_client = Minio(
    minio_cfg.host,
    access_key=minio_cfg.access_key,
    secret_key=minio_cfg.secret_key,
    secure=minio_cfg.secure,
    region=minio_cfg.region,
)


def _update_status(report_id: str, **fields) -> Dict[str, Any]:
    key = f"report:{report_id}"
    payload = redis_client.get(key)
    data = json.loads(payload) if payload else {"id": report_id}
    data.update(fields)
    redis_client.set(key, json.dumps(data))
    return data


@celery_app.task(name="report.generate")
def generate_report(report_id: str, context: Dict[str, Any]):
    logger.info("Generating report %s", report_id)
    _update_status(report_id, status="processing", started_at=datetime.utcnow().isoformat())
    try:
        report_body = {
            "report_id": report_id,
            "analysis_run_id": context.get("analysis_run_id"),
            "heatmap_key": context.get("heatmap_key"),
            "imagery_key": context.get("imagery_key"),
            "stats": context.get("stats"),
            "conclusion": context.get("conclusion"),
            "generated_at": datetime.utcnow().isoformat(),
            "links": {
                "heatmap": context.get("heatmap_key"),
                "imagery": context.get("imagery_key"),
            },
        }
        payload = json.dumps(report_body, ensure_ascii=False).encode("utf-8")
        object_key = f"reports/{report_id}.json"
        minio_client.put_object(
            minio_cfg.bucket_reports,
            object_key,
            BytesIO(payload),
            len(payload),
            content_type="application/json",
        )
        state = _update_status(
            report_id,
            status="completed",
            completed_at=datetime.utcnow().isoformat(),
            report_key=object_key,
        )
        return state
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to generate report %s: %s", report_id, exc)
        _update_status(
            report_id,
            status="failed",
            completed_at=datetime.utcnow().isoformat(),
            error=str(exc),
        )
        raise

