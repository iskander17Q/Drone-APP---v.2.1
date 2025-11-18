## Drone APP v2.1

Комплекс решения для анализа аэрофотоснимков. Состоит из монолита, классического проекта и нового микросервисного слоя.

- `Monolith/` – Flask + Celery backend, повторяющий логику desktop.
- `OLD/` – PyQt5-приложение и библиотека обработки изображений (`image_processing.py` и др.).
- `Microservice/` – архитектура на FastAPI/Celery/MinIO для горизонтального масштабирования.

---

## Структура

```
Monolith/        # REST API и Celery-задачи в одном сервисе
Microservice/    # gateway, imagery, analysis, report + воркеры
OLD/             # исходный desktop и алгоритмы расчётов
```

---

## Быстрый старт (монолит)

```bash
cd Monolith
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m Monolith.manage init-db
python -m Monolith.run  # по умолчанию порт 5000 
```

Ключевые эндпоинты:
- `POST /imagery` – загрузка снимка.
- `POST /analysis-runs` – запуск анализа (ставит Celery-задачу).
- `POST /reports` – генерация отчёта (PDF).

---

## Быстрый старт (микросервисы)

Запустите:
   ```bash
   cd Microservice
   docker compose up -d --build
   curl http://localhost:8081/api/ping
   ```

### Smoke-тест

```bash
# загрузка снимка в imagery-service (MinIO/Redis)
curl -F "file=@/ABS/PATH/field.jpg" http://localhost:8081/imagery
# -> возьмите imagery_id

# запуск анализа (NDVI_emp + автогенерация отчёта)
curl -X POST -H "Content-Type: application/json" \
  -d '{"imagery_id":"<IMAGERY_ID>","index_type":"NDVI_emp","auto_report":true}' \
  http://localhost:8081/analysis-runs

# статус анализа
curl http://localhost:8081/analysis-runs/<RUN_ID>

# статус отчёта
curl http://localhost:8081/reports/<REPORT_ID>
```

---

## Технологии

- **API**: FastAPI, Flask
- **Фоновые задачи**: Celery + Redis
- **Хранилища**: SQLite/PostgreSQL (монолит), Redis/MinIO (микросервисы)
- **Обработка изображений**: `OLD/image_processing.py` (NDVI, VARI, GLI, теплокарты)

---

