FROM python:3.11-slim

WORKDIR /app

COPY app/requirements-docs.txt .

RUN pip install --no-cache-dir -r requirements-docs.txt

COPY . .

WORKDIR /app/app

CMD ["python", "main.py"]

EXPOSE 8080
