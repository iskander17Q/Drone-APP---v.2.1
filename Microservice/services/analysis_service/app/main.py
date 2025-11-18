import json
from typing import Any, Dict
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from redis.asyncio import Redis

from services.analysis_service.worker.app import run_analysis
from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Analysis Service", version="0.1.0")
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


class AnalysisRequest(BaseModel):
    imagery_id: str = Field(..., description="ID загруженного снимка")
    index_type: str = Field(default="NDVI_emp")
    auto_report: bool = Field(default=False)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


async def _fetch_imagery(imagery_id: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.imagery_service_url}/imagery/{imagery_id}", timeout=10
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=404, detail="Снимок не найден") from exc
    return response.json()


async def _save_status(run_id: str, payload: Dict[str, Any]):
    await redis_client.set(f"analysis:{run_id}", json.dumps(payload))


async def _get_status(run_id: str) -> Dict[str, Any]:
    raw = await redis_client.get(f"analysis:{run_id}")
    if not raw:
        raise HTTPException(status_code=404, detail="Запуск анализа не найден")
    return json.loads(raw)


@app.post("/analysis-runs")
async def create_analysis_run(request: AnalysisRequest):
    imagery = await _fetch_imagery(request.imagery_id)
    run_id = str(uuid4())
    status = {
        "id": run_id,
        "imagery_id": request.imagery_id,
        "index_type": request.index_type,
        "status": "queued",
        "auto_report": request.auto_report,
        "imagery_object_key": imagery["object_key"],
        "imagery_bucket": imagery["bucket"],
    }
    await _save_status(run_id, status)
    run_analysis.delay(
        run_id=run_id,
        imagery={
            "bucket": imagery["bucket"],
            "object_key": imagery["object_key"],
            "content_type": imagery.get("content_type"),
        },
        index_type=request.index_type,
        auto_report=request.auto_report,
    )
    return JSONResponse(content=status, status_code=202)


@app.get("/analysis-runs/{run_id}")
async def get_analysis_run(run_id: str):
    status = await _get_status(run_id)
    return status

