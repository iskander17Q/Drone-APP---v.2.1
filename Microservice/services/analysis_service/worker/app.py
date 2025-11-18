import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import httpx
from celery import Celery
from loguru import logger
from minio import Minio
from redis import Redis

from OLD.image_processing import classify_index, compute_indices, generate_heatmap, load_image
from services.common.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "analysis_worker",
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


def _update_status(run_id: str, **fields):
    key = f"analysis:{run_id}"
    state = redis_client.get(key)
    data = json.loads(state) if state else {"id": run_id}
    data.update(fields)
    redis_client.set(key, json.dumps(data))
    return data


def _download_imagery(bucket: str, object_key: str) -> str:
    response = minio_client.get_object(bucket, object_key)
    suffix = Path(object_key).suffix or ".bin"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        for chunk in response.stream(32 * 1024):
            tmp.write(chunk)
    finally:
        tmp.close()
        response.close()
        response.release_conn()
    return tmp.name


def _upload_heatmap(run_id: str, file_path: str) -> str:
    object_key = f"heatmaps/{run_id}.png"
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as heatmap_file:
        minio_client.put_object(
            minio_cfg.bucket_heatmaps,
            object_key,
            heatmap_file,
            file_size,
            content_type="image/png",
        )
    return object_key


def _normalize_stats(stats: Dict[str, Any]) -> Dict[str, float]:
    return {k: float(v) for k, v in stats.items()}


@celery_app.task(name="analysis.run")
def run_analysis(
    run_id: str,
    imagery: Dict[str, Any],
    index_type: str = "NDVI_emp",
    auto_report: bool = False,
):
    logger.info("Starting analysis %s", run_id)
    _update_status(run_id, status="processing", started_at=datetime.utcnow().isoformat())
    heatmap_path = None
    tmp_image = None
    try:
        tmp_image = _download_imagery(imagery["bucket"], imagery["object_key"])
        image = load_image(tmp_image)
        indices = compute_indices(image)
        if index_type not in indices:
            raise RuntimeError(f"Индекс {index_type} недоступен")
        ndvi_map = indices[index_type]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_heatmap:
            tmp_heatmap_path = tmp_heatmap.name
        generate_heatmap(ndvi_map, tmp_heatmap_path)
        heatmap_path = tmp_heatmap_path
        heatmap_key = _upload_heatmap(run_id, heatmap_path)
        stats, conclusion = classify_index(ndvi_map)
        stats = _normalize_stats(stats)

        status = _update_status(
            run_id,
            status="completed",
            completed_at=datetime.utcnow().isoformat(),
            heatmap_key=heatmap_key,
            heatmap_bucket=minio_cfg.bucket_heatmaps,
            stats=stats,
            conclusion=conclusion,
        )

        if auto_report:
            try:
                httpx.post(
                    f"{settings.report_service_url}/reports",
                    json={
                        "analysis_run_id": run_id,
                        "heatmap_key": heatmap_key,
                        "imagery_key": imagery["object_key"],
                        "stats": stats,
                        "conclusion": conclusion,
                    },
                    timeout=10,
                )
            except httpx.HTTPError as exc:
                logger.error("Failed to request auto-report for %s: %s", run_id, exc)

        return status
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Analysis %s failed: %s", run_id, exc)
        _update_status(
            run_id,
            status="failed",
            error=str(exc),
            completed_at=datetime.utcnow().isoformat(),
        )
        raise
    finally:
        if tmp_image and os.path.exists(tmp_image):
            os.unlink(tmp_image)
        if heatmap_path and os.path.exists(heatmap_path):
            os.unlink(heatmap_path)

