## Микросервисная архитектура стекa анализа аэрофотоснимков

### Цели
- развязать загрузку снимков, вычислительные задачи и генерацию отчётов;
- обеспечить горизонтальное масштабирование тяжёлых воркеров;
- упростить замену хранилища файлов (локальный диск ↔️ MinIO/S3);
- сохранить совместимость с текущими модулями анализа (`OLD/*`).

### Сервисы
| Сервис | Назначение | Хранилище | Протоколы |
| --- | --- | --- | --- |
| `api-gateway` | публичный REST/GraphQL слой, валидация, аутентификация, маршрутизация вызовов | stateless | HTTP, gRPC (внутренний) |
| `imagery-service` | загрузка и каталогизация снимков, управление метаданными | PostgreSQL (`imagery_db`), MinIO bucket `imagery` | HTTP (от gateway), gRPC, события `imagery.created` |
| `analysis-service` | постановка задач анализа, оркестрация пайплайна | PostgreSQL (`analysis_db`), Redis Streams/Queue | HTTP/gRPC, события `analysis.*` |
| `analysis-worker` | Celery/Arq воркеры, которые вызывают `OLD.image_processing` и генерируют NDVI/теплокарты | Redis (broker/result), MinIO | Celery |
| `report-service` | CRUD отчётов, хранение PDF-метаданных | PostgreSQL (`report_db`), MinIO bucket `reports` | HTTP/gRPC, события `report.*` |
| `report-worker` | генерация PDF по готовому анализу | Redis, MinIO | Celery |
| `minio` | объектное хранилище raw-файлов, теплокарт, отчётов | дисковый том `storage` | S3 API |
| `redis` | брокер задач + кэш | — | RESP |

Каждый сервиса имеет собственную БД (паттерн Database per Service). Коммуникация — синхронные REST/gRPC вызовы через gateway + асинхронные события в Redis Streams.

### Поток данных
1. Клиент загружает снимок → `api-gateway` → `imagery-service`. Файл кладётся в MinIO (`imagery`), метаданные — в PostgreSQL.
2. Клиент создаёт `analysis-run` → `analysis-service` записывает сущность и публикует событие `analysis.requested`.
3. `analysis-worker` подхватывает задачу, вытаскивает файл из MinIO, запускает `OLD.image_processing`, пишет результаты/теплокарту обратно в MinIO (`heatmaps`) и обновляет статус в `analysis-service`.
4. При `auto_report=true` `analysis-service` публикует `report.requested`. `report-worker` генерирует PDF (используя `OLD.styles` и `reportlab`), сохраняет в MinIO (`reports`) и уведомляет `report-service`.
5. Все пользователи взаимодействуют только с gateway; он агрегирует данные и отдаёт статусы.

### Технологии по умолчанию
- FastAPI + Pydantic v2 для всех REST/gRPC слоёв;
- Celery + Redis для фоновых задач (в дальнейшем допускается NATS/JetStream);
- PostgreSQL 16 с отдельными схемами;
- MinIO в разработке, далее S3;
- OpenTelemetry для трассировки; Prometheus + Grafana для метрик.

### Локальная разработка
```
docker compose up --build
```
Команда поднимет:
- сервисы `api-gateway`, `imagery-service`, `analysis-service`, `report-service`;
- Celery-воркеры `analysis-worker`, `report-worker`;
- инфраструктуру (`redis`, `minio`, `minio-mc`, три PostgreSQL инстанса).

Переменные окружения задаются через `.env` в корне `Microservice/` (см. `env.example`).

### Структура каталога
```
Microservice/
  docker-compose.yml
  README.md
  services/
    api_gateway/
      app/main.py
      requirements.txt
    imagery_service/
      app/main.py
      requirements.txt
    analysis_service/
      app/main.py
      worker/worker.py
      requirements.txt
    report_service/
      app/main.py
      worker/worker.py
      requirements.txt
    common/
      __init__.py
      settings.py        # shared pydantic модели конфигурации
```

На следующем шаге планируется вынести общие DTO/события в пакет `services/common`.


