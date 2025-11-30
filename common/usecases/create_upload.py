from __future__ import annotations

from typing import TYPE_CHECKING

from ..domain.models import Upload, UploadStatus

if TYPE_CHECKING:
    from ..adapters.events import IEventPublisher
    from ..adapters.file_storage import IFileStorage
    from ..adapters.storage import IUnitOfWork


async def create_upload_usecase(
    uow: IUnitOfWork,
    file_storage: IFileStorage,
    event_publisher: IEventPublisher,
    upload_file_bytes: bytes,
    upload_filename: str,
    *,
    has_validation: bool,
) -> Upload:
    upload_storage = uow.upload_storage
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

    await event_publisher.publish_event(
        event_name="parse_upload",
        data={
            "upload_id": upload.upload_id,
        },
    )

    return upload
