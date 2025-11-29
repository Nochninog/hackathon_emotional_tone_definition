from sqlalchemy.ext.asyncio import AsyncSession

from ...adapters.storage import IUnitOfWork

from .text_storage import SqlAlchemyTextStorage
from .uploads_storage import SqlAlchemyUploadStorage
from .validation_storage import SqlAlchemyValidationStorage


class SqlAlchemyUnitOfWork(IUnitOfWork):
    __session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._text_storage = SqlAlchemyTextStorage(session)
        self._upload_storage = SqlAlchemyUploadStorage(session)
        self._validation_storage = SqlAlchemyValidationStorage(session)

        self.__session = session

    async def commit(self) -> None:
        await self.__session.commit()
