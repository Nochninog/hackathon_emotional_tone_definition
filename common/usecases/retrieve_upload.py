from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..adapters.storage import IUnitOfWork
    from ..domain.models import Upload


async def retrieve_upload_usecase(
    uow: IUnitOfWork,
    *,
    upload_id: int,
) -> Sequence[Upload]:
    upload_storage = uow.upload_storage
    return await upload_storage.get_upload_by_id(upload_id)
