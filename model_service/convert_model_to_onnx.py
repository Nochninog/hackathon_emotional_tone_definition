from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from pathlib import Path
import os

def convert_model_to_onnx():
    current_dir = Path(__file__).parent
    model_path = current_dir.parent / 'classification_models' / 'rubert_sentiment_v2'
    # model_path = "../classification_models/rubert_sentiment/"

    # Загружаем модель и токенизатор
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    model.eval()

    # Создаем пример входных данных
    # dummy_input = "Пример текста для конвертации"
    # inputs = tokenizer(dummy_input, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Создаем пример батча из 32 текстов
    batch_size = 32
    dummy_texts = ["Пример текста"] * batch_size

    inputs = tokenizer(
        dummy_texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )

    # Экспортируем в ONNX
    # onnx_path = "./model_service/rubert_sentiment.onnx"
    output_dir = "./model_service/onnx_model_package"
    os.makedirs(output_dir, exist_ok=True)

    # Сохраняем ONNX модель
    onnx_path = os.path.join(output_dir, "model.onnx")

    torch.onnx.export(
        model,
        (inputs['input_ids'], inputs['attention_mask']),
        onnx_path,
        input_names=['input_ids', 'attention_mask'],
        output_names=['logits'],
        dynamic_axes={
            'input_ids': {0: 'batch_size', 1: 'sequence_length'},
            'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
            'logits': {0: 'batch_size'}
        },
        opset_version=12,
        export_params=True
    )

    tokenizer.save_pretrained(output_dir)

    print(f"Модель сохранена как: {onnx_path}")
    return onnx_path


if __name__ == "__main__":
    convert_model_to_onnx()

# convert_model_to_onnx.py
# import os
# from pathlib import Path
# from transformers import AutoModelForSequenceClassification, AutoTokenizer
# import torch
#
#
# def convert_model_to_onnx():
#     # Загружаем модель
#     model_path = "./rubert_sentiment_hf"
#     tokenizer = AutoTokenizer.from_pretrained(model_path)
#     model = AutoModelForSequenceClassification.from_pretrained(model_path)
#     model.eval()
#
#     # Создаем общую папку для ONNX модели и токенизатора
#     output_dir = "./onnx_model_package"
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Сохраняем ONNX модель
#     onnx_path = os.path.join(output_dir, "model.onnx")
#
#     # Экспортируем в ONNX...
#     torch.onnx.export(
#         model,
#         (inputs['input_ids'], inputs['attention_mask']),
#         onnx_path,
#         # ... остальные параметры
#     )
#
#     # Сохраняем токенизатор в ТУ ЖЕ папку
#     tokenizer.save_pretrained(output_dir)
#
#     # Сохраняем конфиг для информации о лейблах
#     model.config.save_pretrained(output_dir)
#
#     print(f"Все файлы сохранены в: {output_dir}")
#
#
# convert_model_to_onnx()