from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .upload import Upload
    from .validation import Validation


class TextStatus(StrEnum):
    NEW = "new"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"


@dataclass
class Text:
    text_id: int
    upload_id: int

    status: TextStatus
    content: str
    predicted_label: int | None = None
    src: str | None = None

    upload: Upload | None = None
    validation: Validation | None = None
