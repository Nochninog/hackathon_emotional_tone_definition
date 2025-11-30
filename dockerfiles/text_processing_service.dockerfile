FROM python:3.13.8-slim-trixie AS runtime

WORKDIR /app

RUN pip install uv

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --group=ml

COPY ./classification_models/rubert_sentiment_v2 ./classification_models/rubert_sentiment_v2
COPY ./app ./app/
COPY ./common ./common/

ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH=/app

RUN mkdir ./uploads

