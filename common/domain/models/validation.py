from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Validation:
    validation_id: int
    text_id: int

    label: int
