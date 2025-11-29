from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from ...adapters.storage import IValidationStorage
from ..mappers import (
    validation_orm_to_model,
    validation_orms_to_models,
)
from ..models import ValidationORM

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

    from ...domain.models import Validation


class SqlAlchemyValidationStorage(IValidationStorage):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_validations(
        self,
        text_ids: Iterable[int],
        labels: Iterable[int],
    ) -> Sequence[Validation]:
        validations = tuple(
            ValidationORM(
                text_id=text_id,
                label=label,
            )
            for text_id, label in zip(text_ids, labels, strict=False)
        )

        self._session.add_all(validations)
        await self._session.flush()

        return validation_orms_to_models(validations)

    async def get_validation_for_text(
        self,
        text_id: int,
    ) -> Validation:
        query = select(ValidationORM).where(ValidationORM.text_id == text_id)
        validation = await self._session.scalar(query)

        if validation is None:
            raise ValueError(f"Validation for text_id={text_id} not found")

        return validation_orm_to_model(validation)

    async def get_validations_for_texts(
        self,
        text_ids: Iterable[int],
    ) -> Sequence[Validation]:
        query = (
            select(ValidationORM)
            .where(ValidationORM.text_id.in_(list(text_ids)))
        )
        validations = await self._session.scalars(query)

        return validation_orms_to_models(validations)
