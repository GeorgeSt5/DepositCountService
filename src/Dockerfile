FROM python:3.7-slim as builder

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN apt-get update && \
       apt-get install -y --no-install-recommends gcc python3-venv python3-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.7-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN apt-get update && apt-get install
RUN pip install --no-cache /wheels/*

COPY . .

EXPOSE 8000