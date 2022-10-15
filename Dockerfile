FROM python:3.7-alpine

WORKDIR /app

COPY ./public .

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]