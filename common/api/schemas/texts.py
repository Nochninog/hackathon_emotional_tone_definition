from __future__ import annotations

from pydantic import BaseModel, Field

from ...domain.models.text import TextStatus


class SText(BaseModel):
    text_id: int
    upload_id: int

    status: TextStatus
    content: str
    predicted_label: int | None = Field(default=None)
    src: str | None = Field(default=None)
