from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


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
