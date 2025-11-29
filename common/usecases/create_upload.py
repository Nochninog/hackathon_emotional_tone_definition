from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.models import Upload, UploadStatus

if TYPE_CHECKING:
    from ..adapters.events import IEventPublisher
    from ..adapters.file_storage import IFileStorage
    from ..adapters.parser import IUploadParser
    from ..adapters.storage import IUnitOfWork


async def create_upload_usecase(
    uow: IUnitOfWork,
    file_storage: IFileStorage,
    event_publisher: IEventPublisher,
    upload_parser: IUploadParser,
    upload_file_bytes: bytes,
    upload_filename: str,
    *,
    has_validation: bool,
) -> Upload:
    upload_storage = uow.upload_storage
    text_storage = uow.text_storage
    validation_storage = uow.validation_storage
    upload = await upload_storage.create_upload(
        status=UploadStatus.PROCESSING,
        filename=upload_filename,
        has_validation=has_validation,
    )
    await uow.commit()

    await file_storage.save_upload_file(
        content=upload_file_bytes,
        upload_id=upload.upload_id,
    )

    if has_validation:
        text_items_with_validations = upload_parser.parse_upload_file_with_validation(
            upload_file_bytes,
        )
        texts = await text_storage.create_texts(
            upload_id=upload.upload_id,
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
            upload_id=upload.upload_id,
            contents=(item.text for item in text_items),
            srcs=(item.src for item in text_items),
        )
    await uow.commit()

    await event_publisher.publish_event(
        event_name="process_upload",
        data={
            "upload_id": upload.upload_id,
        },
    )

    return upload
