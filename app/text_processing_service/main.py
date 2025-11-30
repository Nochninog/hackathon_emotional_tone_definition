from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from common.database.adapters import SqlAlchemyUnitOfWorkFactory
from common.database.connection import create_engine, create_session_maker
from common.local_file_storage.adapters import LocalFileStorage
from common.message_queue.adapters import AioPikaEventConsumer, AioPikaEventPublisher
from common.parser.adapters import PandasCsvUploadParser
from common.rubert_classifier.adapters import RubertTextClassifier
from common.usecases import process_upload_usecase, parse_upload_usecase

from .env import amqp_url, db_url

if TYPE_CHECKING:
    from common.adapters.events import StartUploadProcessingEvent

load_dotenv()

engine = create_engine(
    db_url=db_url,
)
session_maker = create_session_maker(engine)

unit_of_work_factory = SqlAlchemyUnitOfWorkFactory(session_maker=session_maker)
text_classifier = RubertTextClassifier(
    path_to_rubert_model="./classification_models/rubert_sentiment_v2",
)
upload_parser = PandasCsvUploadParser()
file_storage = LocalFileStorage("./uploads")

event_consumer = AioPikaEventConsumer(amqp_url=amqp_url, queue_name="text_processing")
event_publisher = AioPikaEventPublisher(amqp_url=amqp_url)

async def run_process_upload_usecase(data: StartUploadProcessingEvent) -> None:
    async with unit_of_work_factory.with_unit_of_work() as uow:
        await process_upload_usecase(
            uow=uow,
            text_classifier=text_classifier,
            upload_id=data["upload_id"],
        )

async def run_parse_upload_usecase(data: StartUploadProcessingEvent) -> None:
    async with unit_of_work_factory.with_unit_of_work() as uow:
        await parse_upload_usecase(
            uow=uow,
            file_storage=file_storage,
            upload_parser=upload_parser,
            upload_id=data["upload_id"],
            event_publisher=event_publisher,
        )

event_consumer.register_event("process_upload", run_process_upload_usecase)
event_consumer.register_event("parse_upload", run_parse_upload_usecase)

async def main() -> None:
    await event_consumer.connect()

    await event_consumer.start_consuming()
    await asyncio.Future()

    await event_consumer.close()

if __name__ == "__main__":
    asyncio.run(main())
