from fastapi import FastAPI
from fastapi.responses import JSONResponse

from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Report Service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.post("/reports")
async def create_report(payload: dict):
    return JSONResponse(
        content={
            "id": "stub-report-id",
            "analysis_run_id": payload.get("analysis_run_id"),
            "status": "queued",
        },
        status_code=202,
    )

