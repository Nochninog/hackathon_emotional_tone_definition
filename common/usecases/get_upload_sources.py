from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..adapters.storage import IUnitOfWork


async def get_upload_sources_usecase(
    uow: IUnitOfWork,
    *,
    upload_id: int,
) -> Sequence[str]:
    text_storage = uow.text_storage
    return await text_storage.get_text_sources_by_upload_id(upload_id)
