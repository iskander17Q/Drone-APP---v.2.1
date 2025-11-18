from celery import Celery

from services.common.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "analysis_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task(name="analysis.run")
def run_analysis(run_id: str, options: dict | None = None):
    # Здесь будет интеграция с OLD.image_processing для фактического анализа.
    return {
        "run_id": run_id,
        "status": "completed",
        "options": options or {},
    }

