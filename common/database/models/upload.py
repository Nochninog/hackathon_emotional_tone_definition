from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.models import UploadStatus
from ._base import Base

if TYPE_CHECKING:
    from datetime import datetime

    from .text import TextORM


class UploadORM(Base):
    __tablename__ = "uploads"

    upload_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[UploadStatus] = mapped_column(Enum(UploadStatus), nullable=False)
    has_validation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)

    texts: Mapped[list["TextORM"]] = relationship(  # noqa: UP037
        back_populates="upload",
        cascade="all, delete-orphan",
    )

