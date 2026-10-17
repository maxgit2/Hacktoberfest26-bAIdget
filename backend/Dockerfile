FROM python:3.12-slim

WORKDIR /app

COPY environment.yml .
RUN sed -n 's/^      - //p' environment.yml > /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY app app

RUN useradd --create-home appuser
USER appuser

ENV PORT=8080
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
