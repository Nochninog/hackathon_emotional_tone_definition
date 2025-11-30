from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


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


@dataclass
class UploadProcessingProgress:
    total_texts: int
    processed_texts: int
