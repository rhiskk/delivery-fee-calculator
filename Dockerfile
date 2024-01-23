FROM python:3.12

WORKDIR /code

COPY requirements.txt ./
COPY dev-requirements.txt ./

RUN pip install -r requirements.txt
RUN pip install -r dev-requirements.txt

COPY app /code/app/
COPY tests /code/tests
