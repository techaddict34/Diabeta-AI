FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "from notebooks.loadData import extract_n_chunks; from notebooks.vectorEmbed import build_vector_db; extract_n_chunks(); build_vector_db()"


EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]