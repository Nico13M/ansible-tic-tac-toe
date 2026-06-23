FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml Readme.md ./
COPY tic_tac_toe_ynov ./tic_tac_toe_ynov

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

EXPOSE 8000

CMD ["gunicorn", "tic_tac_toe_ynov.app:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
