FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8083

COPY app.py .

CMD ["python", "app.py"]