from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from ...adapters.storage import IUnitOfWork, IUnitOfWorkFactory
from .text_storage import SqlAlchemyTextStorage
from .uploads_storage import SqlAlchemyUploadStorage
from .validation_storage import SqlAlchemyValidationStorage

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SqlAlchemyUnitOfWork(IUnitOfWork):
    __session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._text_storage = SqlAlchemyTextStorage(session)
        self._upload_storage = SqlAlchemyUploadStorage(session)
        self._validation_storage = SqlAlchemyValidationStorage(session)

        self.__session = session

    async def commit(self) -> None:
        await self.__session.commit()


class SqlAlchemyUnitOfWorkFactory(IUnitOfWorkFactory[SqlAlchemyUnitOfWork]):
    __session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self.__session_maker = session_maker

    @asynccontextmanager
    async def with_unit_of_work(self) -> AsyncGenerator[SqlAlchemyUnitOfWork]:
        async with self.__session_maker() as session:
            uow = SqlAlchemyUnitOfWork(session=session)
            yield uow
