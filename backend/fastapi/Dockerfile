FROM python:3.12-slim AS base

FROM base AS builder

RUN apt-get update && apt-get upgrade -y  \
    && apt-get install python3-dev -y  \
    && apt-get install libc-dev  \
    && apt-get install gcc -y

RUN pip install "poetry" && poetry config virtualenvs.in-project true

WORKDIR /install

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root

FROM base

ENV VIRTUAL_ENV=/install/.venv \
    PATH="/install/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /app_dir

WORKDIR /app_dir

EXPOSE 8000

CMD ["./start_web.sh"]
