FROM python:3.7-alpine

WORKDIR /app

COPY ./backend-flask .

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]