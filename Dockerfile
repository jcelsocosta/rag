FROM python:3.12.3-slim

ENV POETRY_VERSION=2.0.1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        git \
        curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.in-project true

RUN poetry install

RUN poetry run python -m spacy download pt_core_news_sm

EXPOSE 3032

CMD ["poetry", "run", "server"]
