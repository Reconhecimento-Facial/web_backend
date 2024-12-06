FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . /app

RUN chmod +x /app/entrypoint.sh && \
    pip install poetry && \
    poetry install --no-interaction --no-ansi

EXPOSE 8000