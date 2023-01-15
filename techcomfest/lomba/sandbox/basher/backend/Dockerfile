FROM python:3.10.8-bullseye

WORKDIR /app

COPY flag.txt /
COPY requirements.txt .
COPY src src
COPY main.py .

RUN pip install -r requirements.txt

USER 404:404

CMD ["python3", "main.py", "8000"]