FROM python:3.9-slim
WORKDIR /Reunion

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]