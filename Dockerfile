FROM python:3.12-slim as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip pip-tools

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.12-slim

WORKDIR /usr/src/app

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

RUN chown -R app:app /usr/src/app

USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "parking_service.wsgi:application"]
