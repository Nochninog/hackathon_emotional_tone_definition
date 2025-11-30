from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from fastapi import FastAPI

from common.database.adapters import SqlAlchemyUnitOfWorkFactory
from common.database.connection import create_engine, create_session_maker, dispose_engine
from common.local_file_storage.adapters import LocalFileStorage
from common.message_queue.adapters import AioPikaEventPublisher

from .controller import UploadsController
from .env import amqp_url, db_url

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

engine = create_engine(
    db_url=db_url,
)
session_maker = create_session_maker(engine)

unit_of_work_factory = SqlAlchemyUnitOfWorkFactory(session_maker=session_maker)
file_storage = LocalFileStorage("./uploads")
event_publisher = AioPikaEventPublisher(amqp_url=amqp_url)

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


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
