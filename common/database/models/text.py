from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.models import TextStatus
from ._base import Base

if TYPE_CHECKING:
    from .upload import UploadORM
    from .validation import ValidationORM


class TextORM(Base):
    __tablename__ = "texts"

    text_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.upload_id"), nullable=False)

    status: Mapped[TextStatus] = mapped_column(Enum(TextStatus), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    predicted_label: Mapped[int | None] = mapped_column(String, nullable=True)
    src: Mapped[str | None] = mapped_column(String, nullable=True)

    upload: Mapped["UploadORM"] = relationship(back_populates="texts")  # noqa: UP037
    validation: Mapped["ValidationORM"] = relationship(back_populates="text")  # noqa: UP037
