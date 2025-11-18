from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Drone API Gateway", version="0.1.0")


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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.imagery_service_url}/imagery",
                files={"file": (file.filename, await file.read(), file.content_type)},
                data={k: v for k, v in metadata.items() if v is not None},
                timeout=30,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502, detail=f"Imagery service unavailable: {exc}"
            ) from exc
    return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/analysis-runs")
async def create_analysis_run(payload: Dict[str, Any]) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.analysis_service_url}/analysis-runs",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502, detail=f"Analysis service unavailable: {exc}"
            ) from exc
    return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/reports")
async def request_report(payload: Dict[str, Any]) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.report_service_url}/reports", json=payload, timeout=10
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502, detail=f"Report service unavailable: {exc}"
            ) from exc
    return JSONResponse(content=response.json(), status_code=response.status_code)

