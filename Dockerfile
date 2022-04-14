FROM python:3

WORKDIR /app

COPY . .

RUN pip install discord requests

CMD python src/main.py