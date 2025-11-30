from __future__ import annotations

import logging
from math import ceil
from typing import TYPE_CHECKING

from ..domain.models import Text, TextStatus, UploadStatus

if TYPE_CHECKING:
    from ..adapters.classifier import ITextClassifier
    from ..adapters.storage import IUnitOfWork


MAX_BATCH_SIZE = 100


async def handle_batch(
    uow: IUnitOfWork,
    text_classifier: ITextClassifier,
    texts_batch: list[Text],
) -> bool:
    has_error = False
    text_storage = uow.text_storage
    try:
        predicted_labels = await text_classifier.predict_labels_for_texts(
            texts=(text.content for text in texts_batch),
        )
        for predicted_label, text_item in zip(
            predicted_labels,
            texts_batch,
            strict=True,
        ):
            await text_storage.update_text_status(
                text_id=text_item.text_id,
                status=TextStatus.DONE,
            )
            await text_storage.update_text_predicted_label(
                text_id=text_item.text_id,
                predicted_label=predicted_label,
            )

    except Exception as e:
        print(e)
        has_error = True
        for text_item in texts_batch:
            await text_storage.update_text_status(
                text_id=text_item.text_id,
                status=TextStatus.ERROR,
            )

    await uow.commit()

    return has_error

async def process_upload_usecase(
    uow: IUnitOfWork,
    text_classifier: ITextClassifier,
    upload_id: int,
) -> None:
    upload_storage = uow.upload_storage
    text_storage = uow.text_storage

    total_texts = await text_storage.count_texts_by_upload_id(upload_id=upload_id)
    logging.warning(total_texts)
    total_batches = ceil(total_texts / MAX_BATCH_SIZE)
    has_error = False
    for batch_number in range(total_batches):
        texts_batch = await text_storage.get_texts_by_upload_id(
            upload_id=upload_id,
            limit=MAX_BATCH_SIZE,
            offset=batch_number * MAX_BATCH_SIZE,
        )
        has_error = await handle_batch(
            uow=uow,
            text_classifier=text_classifier,
            texts_batch=texts_batch,
        ) or has_error

    await upload_storage.update_upload_status(
        upload_id=upload_id,
        status=UploadStatus.ERROR if has_error else UploadStatus.DONE,
    )

    await uow.commit()

