import json
from typing import Any, Dict, Optional
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis.asyncio import Redis

from services.common.settings import get_settings
from services.report_service.worker.app import generate_report

settings = get_settings()
app = FastAPI(title="Report Service", version="0.1.0")
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


class ReportRequest(BaseModel):
    analysis_run_id: str
    heatmap_key: Optional[str] = None
    imagery_key: Optional[str] = None
    stats: Optional[Dict[str, float]] = None
    conclusion: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.service_name}


async def _fetch_analysis(run_id: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.analysis_service_url}/analysis-runs/{run_id}", timeout=10
        )
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Анализ не найден")
        resp.raise_for_status()
    return resp.json()


async def _save_status(report_id: str, payload: Dict[str, Any]):
    await redis_client.set(f"report:{report_id}", json.dumps(payload))


async def _get_status(report_id: str) -> Dict[str, Any]:
    raw = await redis_client.get(f"report:{report_id}")
    if not raw:
        raise HTTPException(status_code=404, detail="Отчёт не найден")
    return json.loads(raw)


@app.post("/reports")
async def create_report(request: ReportRequest):
    analysis = await _fetch_analysis(request.analysis_run_id)
    if analysis.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Анализ ещё не завершён")

    report_id = str(uuid4())
    payload = {
        "id": report_id,
        "analysis_run_id": request.analysis_run_id,
        "status": "queued",
        "heatmap_key": request.heatmap_key or analysis.get("heatmap_key"),
        "imagery_key": request.imagery_key or analysis.get("imagery_object_key"),
        "stats": request.stats or analysis.get("stats"),
        "conclusion": request.conclusion or analysis.get("conclusion"),
    }
    if not payload["heatmap_key"]:
        raise HTTPException(status_code=400, detail="Нет теплокарты для отчёта")
    if not payload["imagery_key"]:
        raise HTTPException(
            status_code=400, detail="Нет исходного снимка для формирования отчёта"
        )
    await _save_status(report_id, payload)
    generate_report.delay(report_id, payload)
    return JSONResponse(content=payload, status_code=202)


@app.get("/reports/{report_id}")
async def get_report(report_id: str):
    return await _get_status(report_id)

