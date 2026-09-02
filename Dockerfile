FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# vector_db is prebuilt locally and committed to the repo, so it just
# ships with the image instead of being computed in the memory-constrained
# build container.

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]