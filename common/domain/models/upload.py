from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .text import Text


class UploadStatus(StrEnum):
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"


@dataclass
class Upload:
    upload_id: int
    uploaded_at: datetime
    status: UploadStatus
    filename: str
    has_validation: bool = False

    texts: list[Text] = field(default_factory=list)
