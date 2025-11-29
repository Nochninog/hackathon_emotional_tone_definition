from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from .text_storage import ITextStorage
    from .uploads_storage import IUploadStorage
    from .validation_storage import IValidationStorage


class IUnitOfWorkFactory[UnitOfWork: IUnitOfWork](ABC):
    @asynccontextmanager
    @abstractmethod
    def with_unit_of_work(self) -> AsyncGenerator[UnitOfWork]:
        raise NotImplementedError


class IUnitOfWork(ABC):
    _text_storage: ITextStorage
    _upload_storage: IUploadStorage
    _validation_storage: IValidationStorage

    @property
    def text_storage(self) -> ITextStorage:
        return self._text_storage

    @property
    def upload_storage(self) -> IUploadStorage:
        return self._upload_storage

    @property
    def validation_storage(self) -> IValidationStorage:
        return self._validation_storage

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
