FROM python:3.8
# EXPOSE 8080

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["uwsgi", "app.ini"]
# CMD ["python", "./app.py"]