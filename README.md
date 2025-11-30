Требования для запуска системы: установленные docker и python 3.13+
Для запуска приложения необходимо установить uv:

```bash
pip install uv
```

Далее необходимо синхронизировать окружение

```bash
uv sync
```

Далее необходимо настроить переменные окружения. В корне проекта требуется создать файл .env со следующим содержимым (пароли и имена пользователей могут варьироваться):
```
DB_USER=postgres
DB_PORT=5432
DB_MIGRATION_PORT=5430
DB_MIGRATION_ENGINE=postgresql
DB_PASSWORD=root
DB_NAME=reviews_analysis
DB_MIGRATION_HOST=localhost
DB_HOST=postgres

RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin123
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/
```

После этого необходимо запустить приложение для совершения миграций

```bash
docker compose up -d --build
```

Далее необходимо провести миграции

На Linux/MacOS:
```bash
source .venv\bin\activate
alembic upgrade head
```

На Windows:

```bash
.venv\Scripts\activate
alembic upgrade head
```

Далее необходимо получить архив с весами модели и распаковать в папку classification_models/rubert_sentiment_v2 в корне проекта. Архив можно получить по ссылке: https://disk.yandex.ru/d/Bdv9SX-qNSVlJA

После этого необходимо перезапустить приложение
```bash
docker compose down
docker compose up
```