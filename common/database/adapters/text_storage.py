from collections.abc import Iterable, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models import Text, TextStatus
from ..models import TextORM


class SqlAlchemyTextStorage():
    def __init__(self, session: AsyncSession):
        self._session = session

    # ---------------------------
    # Create
    # ---------------------------
    async def create_texts(
        self,
        upload_id: int,
        contents: Iterable[str],
    ) -> Sequence[Text]:
        texts = [
            TextORM(
                upload_id=upload_id,
                content=content,
                status=TextStatus.NEW,
            )
            for content in contents
        ]

        self._session.add_all(texts)
        await self._session.flush()   # получаем text_id

        return texts

    # ---------------------------
    # Read
    # ---------------------------
    async def get_texts_by_upload_id(
        self,
        upload_id: int,
    ) -> Sequence[Text]:
        stmt = select(TextORM).where(TextORM.upload_id == upload_id)
        result = await self._session.scalars(stmt)
        return list(result)

    async def get_text_by_id(
        self,
        text_id: int,
    ) -> Text:
        stmt = select(TextORM).where(TextORM.text_id == text_id)
        result = await self._session.scalar(stmt)

        if result is None:
            raise ValueError(f"Text with id={text_id} not found")

        return result

    async def get_texts_by_source(
        self,
        src: str,
    ) -> Sequence[Text]:
        stmt = select(TextORM).where(TextORM.src == src)
        result = await self._session.scalars(stmt)
        return list(result)

    async def get_texts_by_source_and_upload_id(
        self,
        src: str,
        upload_id: int,
    ) -> Sequence[Text]:
        stmt = (
            select(TextORM)
            .where(TextORM.src == src)
            .where(TextORM.upload_id == upload_id)
        )
        result = await self._session.scalars(stmt)
        return list(result)

    # ---------------------------
    # Update
    # ---------------------------
    async def update_text_status(
        self,
        text_id: int,
        status: TextStatus,
    ) -> None:
        stmt = (
            update(TextORM)
            .where(TextORM.text_id == text_id)
            .values(status=status)
        )

        await self._session.execute(stmt)

    async def update_text_predicted_label(
        self,
        text_id: int,
        predicted_label: int,
    ) -> None:
        stmt = (
            update(TextORM)
            .where(TextORM.text_id == text_id)
            .values(predicted_label=str(predicted_label))
        )

        await self._session.execute(stmt)
