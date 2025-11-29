# onnx_inference.py
from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np


class ONNXInference:
    def __init__(self, onnx_model_path: str, max_length: int = 512):
        self.session = ort.InferenceSession(onnx_model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(onnx_model_path)
        self.max_length = max_length  # Сохраняем настройку

    def predict(self, texts: list):
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.max_length,  # ← Указываем здесь
            return_tensors="np"
        )

        onnx_inputs = {
            'input_ids': inputs['input_ids'].astype(np.int64),
            'attention_mask': inputs['attention_mask'].astype(np.int64)
        }

        logits = self.session.run(['logits'], onnx_inputs)[0]
        return np.argmax(logits, axis=1)


# Использование с кастомным max_length
# inference_engine = ONNXInference(
#     onnx_model_path="./rubert_sentiment.onnx",
#     tokenizer_path="./rubert_sentiment_hf",
#     max_length=256  # ← Уменьшаем для скорости
# )



# Использование - только одна папка!
inference_engine = ONNXInference("./model_service")




