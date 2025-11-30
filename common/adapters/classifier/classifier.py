from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


class ITextClassifier(ABC):
    @abstractmethod
    async def predict_labels_for_texts(self, texts: Iterable[str]) -> Iterable[int]:
        raise NotImplementedError
