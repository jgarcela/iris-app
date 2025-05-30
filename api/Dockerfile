FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../database /app/database

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
