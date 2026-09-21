FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


FROM base AS development

COPY requirements.txt requirements-dev.txt ./

RUN pip install \
    --no-cache-dir \
    -r requirements-dev.txt

COPY . .

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]


FROM base AS production

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]