FROM python:3.8-slim-buster

WORKDIR /diagnosticapp

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]
