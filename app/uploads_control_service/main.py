from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from os import environ

from dotenv import load_dotenv
from fastapi import FastAPI

from common.database.adapters import SqlAlchemyUnitOfWorkFactory
from common.database.connection import create_engine, create_session_maker, dispose_engine
from common.local_file_storage.adapters import LocalFileStorage
from common.message_queue.adapters import AioPikaEventPublisher

from .controller import UploadsController

load_dotenv()

engine = create_engine(
    db_url=environ.get("DB_URL") or "",
)
session_maker = create_session_maker(engine)

unit_of_work_factory = SqlAlchemyUnitOfWorkFactory(session_maker=session_maker)
file_storage = LocalFileStorage("./uploads")
event_publisher = AioPikaEventPublisher(amqp_url="amqp://admin:admin123@localhost:5672/")

controller = UploadsController(
    file_storage=file_storage,
    event_publisher=event_publisher,
    unit_of_work_factory=unit_of_work_factory,
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield
    await dispose_engine(engine)

app = FastAPI(
    docs_url="/docs",
    lifespan=lifespan,
)
app.include_router(controller.router)
