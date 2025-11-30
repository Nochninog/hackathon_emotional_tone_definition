from typing import TYPE_CHECKING

from ...adapters.classifier import ITextClassifier
from ..model import RubertModel

if TYPE_CHECKING:
    from collections.abc import Iterable

class RubertTextClassifier(ITextClassifier):
    __model: RubertModel

    def __init__(self, path_to_rubert_model: str) -> None:
        self.__model = RubertModel(path_to_model=path_to_rubert_model)

    async def predict_labels_for_texts(self, texts: "Iterable[str]") -> "Iterable[int]":
        return self.__model.predict_labels(texts=texts)
