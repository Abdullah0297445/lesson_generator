FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y supervisor

WORKDIR /app

COPY pyproject.toml .
RUN pip install .

COPY . .

CMD ["/usr/bin/supervisord"]
