from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from common.domain.models import UploadStatus

if TYPE_CHECKING:
    from ..adapters.events import IEventPublisher
    from ..adapters.file_storage import IFileStorage
    from ..adapters.parser import IUploadParser
    from ..adapters.storage import IUnitOfWork


async def parse_upload_usecase(
    uow: IUnitOfWork,
    file_storage: IFileStorage,
    event_publisher: IEventPublisher,
    upload_parser: IUploadParser,
    upload_id: int,
) -> None:
    text_storage = uow.text_storage
    validation_storage = uow.validation_storage
    upload_storage = uow.upload_storage

    upload = await upload_storage.get_upload_by_id(upload_id=upload_id)

    upload_file_bytes = await file_storage.read_upload_file(upload_id=upload_id)

    try:
        logging.warning("Start parsing upload...")
        if upload.has_validation:
            text_items_with_validations = upload_parser.parse_upload_file_with_validation(
                upload_file_bytes,
            )
            texts = await text_storage.create_texts(
                upload_id=upload_id,
                contents=(item.text for item in text_items_with_validations),
                srcs=(item.src for item in text_items_with_validations),
            )
            await validation_storage.create_validations(
                text_ids=(text.text_id for text in texts),
                labels=(item.label for item in text_items_with_validations),
            )

        else:
            text_items = upload_parser.parse_upload_file(
                upload_file_bytes,
            )
            texts = await text_storage.create_texts(
                upload_id=upload_id,
                contents=(item.text for item in text_items),
                srcs=(item.src for item in text_items),
            )

        await uow.commit()
        await event_publisher.publish_event(
            event_name="process_upload",
            data={
                "upload_id": upload_id,
            },
        )
        logging.warning("Upload parsed")
    except Exception:

        logging.error("Upload parsing failed")
        await upload_storage.update_upload_status(
            upload_id=upload_id,
            status=UploadStatus.ERROR,
        )

        await uow.commit()

