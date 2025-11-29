FROM python:3.13.8-slim-trixie AS runtime

WORKDIR /app

RUN pip install uv

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --no-dev --frozen

COPY ./app ./app/
COPY ./common ./common/

ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH=/app

RUN mkdir ./uploads

EXPOSE 8080
