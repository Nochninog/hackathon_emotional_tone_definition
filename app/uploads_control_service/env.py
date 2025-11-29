from os import environ
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", "5432")
DB_NAME = environ.get("DB_NAME") 

db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RABBITMQ_USER = environ.get("RABBITMQ_USER")
RABBITMQ_PASSWORD = quote_plus(environ.get("RABBITMQ_PASSWORD") or "")
RABBITMQ_HOST = environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = environ.get("RABBITMQ_PORT", "5672")
RABBITMQ_VHOST = quote_plus(environ.get("RABBITMQ_VHOST") or "/")

amqp_url = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}"
    f"@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    f"{RABBITMQ_VHOST}"
)
