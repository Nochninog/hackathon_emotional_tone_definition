from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from ...domain.models import Text, TextStatus


class ITextStorage(ABC):
    @abstractmethod
    async def create_texts(
        self,
        upload_id: int,
        contents: Iterable[str],
    ) -> Sequence[Text]:
        raise NotImplementedError

    @abstractmethod
    async def get_texts_by_upload_id(
        self,
        upload_id: int,
    ) -> Sequence[Text]:
        raise NotImplementedError

    @abstractmethod
    async def get_text_by_id(
        self,
        text_id: int,
    ) -> Text:
        raise NotImplementedError

    @abstractmethod
    async def get_texts_by_source(
        self,
        src: str,
    ) -> Sequence[Text]:
        raise NotImplementedError

    @abstractmethod
    async def get_texts_by_source_and_upload_id(
        self,
        src: str,
        upload_id: int,
    ) -> Sequence[Text]:
        raise NotImplementedError

    @abstractmethod
    async def update_text_status(
        self,
        text_id: int,
        status: TextStatus,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_text_predicted_label(
        self,
        text_id: int,
        predicted_label: int,
    ) -> None:
        raise NotImplementedError
