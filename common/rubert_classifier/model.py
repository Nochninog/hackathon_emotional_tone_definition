
from typing import TYPE_CHECKING

from tqdm import tqdm
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)

if TYPE_CHECKING:
    from collections.abc import Iterable


class RubertModel:
    def __init__(
        self,
        path_to_model: str,
    ) -> None:
        model = AutoModelForSequenceClassification.from_pretrained(
            path_to_model,
            local_files_only=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            path_to_model,
            local_files_only=True,
        )

        self.classifier = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            device=-1,
            max_length=512,
        )

        self.label_map = {
            "LABEL_0": 0,
            "LABEL_1": 1,
            "LABEL_2": 2,
        }

    def predict_labels(self, texts: "Iterable[str]") -> list[int]:
        pred_labels = []
        for text in tqdm(texts):
            result = self.classifier(text, truncation=True)[0]["label"]
            pred_labels.append(self.label_map[result])
        return pred_labels
