FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pymongo pydantic[email]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
