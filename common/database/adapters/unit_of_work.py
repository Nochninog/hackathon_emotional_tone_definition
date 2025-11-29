from __future__ import annotations

from typing import TYPE_CHECKING

from ...adapters.storage import IUnitOfWork
from .text_storage import SqlAlchemyTextStorage
from .uploads_storage import SqlAlchemyUploadStorage
from .validation_storage import SqlAlchemyValidationStorage

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(IUnitOfWork):
    __session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._text_storage = SqlAlchemyTextStorage(session)
        self._upload_storage = SqlAlchemyUploadStorage(session)
        self._validation_storage = SqlAlchemyValidationStorage(session)

        self.__session = session

    async def commit(self) -> None:
        await self.__session.commit()
