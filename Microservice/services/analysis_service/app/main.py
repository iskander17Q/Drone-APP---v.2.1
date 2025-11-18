from fastapi import FastAPI
from fastapi.responses import JSONResponse

from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Analysis Service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.post("/analysis-runs")
async def create_analysis_run(payload: dict):
    # Заглушка: в реальном сервисе сохраняем run в БД и ставим задачу в очередь.
    return JSONResponse(
        content={
            "id": "stub-analysis-id",
            "imagery_id": payload.get("imagery_id"),
            "status": "queued",
        },
        status_code=202,
    )

