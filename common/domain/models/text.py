from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


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


@dataclass
class ToneDistribution:
    positive: int
    negative: int
    neutral: int
