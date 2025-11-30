from __future__ import annotations

from typing import TYPE_CHECKING

from common.domain.models import UploadProcessingProgress

if TYPE_CHECKING:
    from ..adapters.storage import IUnitOfWork


async def get_upload_processing_progress_usecase(
    uow: IUnitOfWork,
    *,
    upload_id: int,
) -> UploadProcessingProgress:
    text_storage = uow.text_storage
    total_texts = await text_storage.count_texts_by_upload_id(
        upload_id=upload_id,
    )
    processed_texts = await text_storage.count_processed_texts_by_upload_id(
        upload_id=upload_id,
    )

    return UploadProcessingProgress(
        total_texts=total_texts,
        processed_texts=processed_texts,
    )
