from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass
class TextItem:
    text: str
    src: str | None = None


@dataclass
class TextItemWithValidation:
    text: str
    label: int
    src: str | None = None


class IUploadParser(ABC):
    @abstractmethod
    def parse_upload_file(self, file_bytes: bytes) -> Sequence[TextItem]:
        raise NotImplementedError

    @abstractmethod
    def parse_upload_file_with_validation(
        self,
        file_bytes: bytes,
    ) -> Sequence[TextItemWithValidation]:
        raise NotImplementedError
