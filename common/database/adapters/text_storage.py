from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import and_, func, select, update

from ...adapters.storage import ITextStorage
from ...domain.models import Text, TextStatus
from ..mappers import text_orm_to_model, text_orms_to_models
from ..models import TextORM

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyTextStorage(ITextStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_texts(
        self,
        upload_id: int,
        contents: Iterable[str],
        srcs: Iterable[str | None],
    ) -> Sequence[Text]:
        texts = tuple(
            TextORM(
                upload_id=upload_id,
                content=content,
                status=TextStatus.NEW,
                src=src,
            )
            for content, src in zip(contents, srcs, strict=True)
        )

        self._session.add_all(texts)
        await self._session.flush()

        return text_orms_to_models(texts)

    async def get_texts_by_upload_id(
        self,
        upload_id: int,
        limit: int = -1,
        offset: int = 0,
    ) -> Sequence[Text]:
        query = select(TextORM).where(TextORM.upload_id == upload_id)
        if limit > 0:
            query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)
        texts = await self._session.scalars(query)
        return text_orms_to_models(texts)

    async def count_texts_by_upload_id(
        self,
        upload_id: int,
    ) -> int:
        query = select(func.count()).select_from(
            select(TextORM).where(TextORM.upload_id == upload_id),
        )
        return await self._session.scalar(query)

    async def get_text_sources_by_upload_id(
        self,
        upload_id: int,
    ) -> Sequence[str]:
        query = (
            select(TextORM.src)
            .where(TextORM.upload_id == upload_id)
            .group_by(TextORM.src)
        )
        return await self._session.scalars(query)

    async def get_predicted_labels_distribution_by_upload_id(
        self,
        upload_id: int,
    ) -> Mapping[int, int]:
        query = (
            select(
                TextORM.predicted_label,
                func.count().label("count"),
            )
            .where(TextORM.upload_id == upload_id)
            .group_by(TextORM.predicted_label)
        )
        rows = await self._session.execute(query)
        distribution = {}
        for (label, count) in rows.all():
            distribution[label] = count
        return distribution

    async def count_processed_texts_by_upload_id(
        self,
        upload_id: int,
    ) -> int:
        query = select(func.count()).select_from(
            select(TextORM).where(and_(
                TextORM.upload_id == upload_id,
                TextORM.predicted_label >= 0,
            )),
        )
        return await self._session.scalar(query)

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
