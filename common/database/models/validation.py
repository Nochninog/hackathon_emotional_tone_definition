from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from .text import TextORM


class ValidationORM(Base):
    __tablename__ = "validations"

    validation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.text_id"), nullable=False)

    label: Mapped[int] = mapped_column(Integer, nullable=False)

    text: Mapped["TextORM"] = relationship(back_populates="validation")  # noqa: UP037
