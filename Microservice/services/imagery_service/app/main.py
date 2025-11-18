import asyncio
import json
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from minio import Minio
from redis.asyncio import Redis

from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Imagery Service", version="0.1.0")

redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
minio_cfg = settings.minio
minio_client = Minio(
    minio_cfg.host,
    access_key=minio_cfg.access_key,
    secret_key=minio_cfg.secret_key,
    secure=minio_cfg.secure,
    region=minio_cfg.region,
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


def _clean_filename(filename: Optional[str]) -> str:
    if not filename:
        return "upload.bin"
    return Path(filename).name


async def _save_metadata(record: Dict[str, Any]):
    key = f"imagery:{record['id']}"
    await redis_client.set(key, json.dumps(record))


async def _get_metadata(imagery_id: str) -> Optional[Dict[str, Any]]:
    raw = await redis_client.get(f"imagery:{imagery_id}")
    return json.loads(raw) if raw else None


@app.post("/imagery")
async def create_imagery(file: UploadFile = File(...)):
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Файл пуст или недоступен")

    imagery_id = str(uuid4())
    safe_name = _clean_filename(file.filename)
    object_key = f"imagery/{imagery_id}/{safe_name}"

    await asyncio.to_thread(
        minio_client.put_object,
        minio_cfg.bucket_imagery,
        object_key,
        BytesIO(data),
        len(data),
        content_type=file.content_type or "application/octet-stream",
    )

    record = {
        "id": imagery_id,
        "original_filename": safe_name,
        "bucket": minio_cfg.bucket_imagery,
        "object_key": object_key,
        "content_type": file.content_type or "application/octet-stream",
        "status": "uploaded",
    }
    await _save_metadata(record)
    return JSONResponse(content=record, status_code=201)


@app.get("/imagery/{imagery_id}")
async def get_imagery(imagery_id: str):
    record = await _get_metadata(imagery_id)
    if not record:
        raise HTTPException(status_code=404, detail="Снимок не найден")
    return record

