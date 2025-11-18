from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from services.common.settings import get_settings

settings = get_settings()
app = FastAPI(title="Imagery Service", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.post("/imagery")
async def create_imagery(file: UploadFile = File(...)):
    # Здесь будет логика сохранения файла в MinIO и записи метаданных в PostgreSQL.
    # Для архитектурного каркаса возвращаем заглушку.
    return JSONResponse(
        content={
            "id": "stub-imagery-id",
            "original_filename": file.filename,
            "status": "uploaded",
        },
        status_code=201,
    )

