FROM python:3.12

WORKDIR /code

COPY requirements.txt ./
COPY requirements-dev.txt ./

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY app /code/app/
COPY tests /code/tests
