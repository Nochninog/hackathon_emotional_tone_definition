from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .text import Text


@dataclass
class Validation:
    validation_id: int
    text_id: int

    label: str

    text: Text | None = None
