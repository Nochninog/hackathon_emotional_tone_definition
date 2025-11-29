from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select, update

from ...adapters.storage import ITextStorage
from ...domain.models import Text, TextStatus
from ..mappers import text_orm_to_model, text_orms_to_models
from ..models import TextORM

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyTextStorage(ITextStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_texts(
        self,
        upload_id: int,
        contents: Iterable[str],
    ) -> Sequence[Text]:
        texts = tuple(
            TextORM(
                upload_id=upload_id,
                content=content,
                status=TextStatus.NEW,
            )
            for content in contents
        )

        self._session.add_all(texts)
        await self._session.flush()

        return text_orms_to_models(texts)

    async def get_texts_by_upload_id(
        self,
        upload_id: int,
    ) -> Sequence[Text]:
        query = select(TextORM).where(TextORM.upload_id == upload_id)
        texts = await self._session.scalars(query)
        return text_orms_to_models(texts)

    async def get_text_by_id(
        self,
        text_id: int,
    ) -> Text:
        query = select(TextORM).where(TextORM.text_id == text_id)
        text = await self._session.scalar(query)

        if text is None:
            raise ValueError(f"Text with id={text_id} not found")

        return text_orm_to_model(text)

    async def get_texts_by_source(
        self,
        src: str,
    ) -> Sequence[Text]:
        query = select(TextORM).where(TextORM.src == src)
        texts = await self._session.scalars(query)
        return text_orms_to_models(texts)

    async def get_texts_by_source_and_upload_id(
        self,
        src: str,
        upload_id: int,
    ) -> Sequence[Text]:
        query = (
            select(TextORM)
            .where(TextORM.src == src)
            .where(TextORM.upload_id == upload_id)
        )
        texts = await self._session.scalars(query)
        return text_orms_to_models(texts)

    async def update_text_status(
        self,
        text_id: int,
        status: TextStatus,
    ) -> None:
        query = (
            update(TextORM)
            .where(TextORM.text_id == text_id)
            .values(status=status)
        )

        await self._session.execute(query)

    async def update_text_predicted_label(
        self,
        text_id: int,
        predicted_label: int,
    ) -> None:
        query = (
            update(TextORM)
            .where(TextORM.text_id == text_id)
            .values(predicted_label=predicted_label)
        )

        await self._session.execute(query)
