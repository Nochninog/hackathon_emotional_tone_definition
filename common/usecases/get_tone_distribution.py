from __future__ import annotations

from typing import TYPE_CHECKING

from common.domain.models import ToneDistribution

if TYPE_CHECKING:
    from ..adapters.storage import IUnitOfWork


async def get_tone_distribution_usecase(
    uow: IUnitOfWork,
    *,
    upload_id: int,
) -> ToneDistribution:
    text_storage = uow.text_storage
    labels_distribution = await text_storage.get_predicted_labels_distribution_by_upload_id(
        upload_id=upload_id,
    )

    return ToneDistribution(
        positive=labels_distribution.get(1, 0),
        negative=labels_distribution.get(2, 0),
        neutral=labels_distribution.get(0, 0),
    )
