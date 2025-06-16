FROM python:3.11-slim

WORKDIR /app
COPY tomodachi_core/ tomodachi_core/
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "tomodachi_core/server/main.py"]
