from celery import Celery

from services.common.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "report_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task(name="report.generate")
def generate_report(report_id: str, analysis_run_id: str):
    # Заглушка: в дальнейшем сюда подключается OLD.report генерация PDF.
    return {
        "report_id": report_id,
        "analysis_run_id": analysis_run_id,
        "status": "generated",
    }

