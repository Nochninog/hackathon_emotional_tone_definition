from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..adapters.storage import IUnitOfWork
    from ..domain.models import Upload


async def list_uploads_usecase(
    uow: IUnitOfWork,
    *,
    search: str,
) -> Sequence[Upload]:
    upload_storage = uow.upload_storage
    return await upload_storage.get_all_uploads_with_search(search=search)
