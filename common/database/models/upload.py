from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

from ...domain.models import UploadStatus

if TYPE_CHECKING:
    from .text import TextORM


class UploadORM(Base):
    __tablename__ = "uploads"

    upload_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[UploadStatus] = mapped_column(Enum(UploadStatus), nullable=False)
    has_validation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)

    texts: Mapped[list["TextORM"]] = relationship(
        back_populates="upload",
        cascade="all, delete-orphan",
    )

