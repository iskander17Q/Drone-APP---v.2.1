from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Drone API Gateway", version="0.1.0")


async def _proxy_request(method: str, url: str, **kwargs) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return JSONResponse(content=response.json(), status_code=response.status_code)


@app.get("/api/ping")
async def ping() -> Dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@app.post("/imagery")
async def upload_imagery(
    file: UploadFile = File(...),
    captured_at: Optional[str] = Form(default=None),
    gps_lat: Optional[float] = Form(default=None),
    gps_lon: Optional[float] = Form(default=None),
) -> JSONResponse:
    metadata: Dict[str, Any] = {
        "captured_at": captured_at,
        "gps_lat": gps_lat,
        "gps_lon": gps_lon,
    }
    return await _proxy_request(
        "POST",
        f"{settings.imagery_service_url}/imagery",
        files={"file": (file.filename, await file.read(), file.content_type)},
        data={k: v for k, v in metadata.items() if v is not None},
    )


@app.post("/analysis-runs")
async def create_analysis_run(payload: Dict[str, Any]) -> JSONResponse:
    return await _proxy_request(
        "POST",
        f"{settings.analysis_service_url}/analysis-runs",
        json=payload,
    )


@app.get("/analysis-runs/{run_id}")
async def get_analysis_run(run_id: str) -> JSONResponse:
    return await _proxy_request(
        "GET",
        f"{settings.analysis_service_url}/analysis-runs/{run_id}",
    )


@app.post("/reports")
async def request_report(payload: Dict[str, Any]) -> JSONResponse:
    return await _proxy_request(
        "POST",
        f"{settings.report_service_url}/reports",
        json=payload,
    )


@app.get("/reports/{report_id}")
async def get_report(report_id: str) -> JSONResponse:
    return await _proxy_request(
        "GET",
        f"{settings.report_service_url}/reports/{report_id}",
    )

