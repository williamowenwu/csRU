FROM python:3.11-slim
WORKDIR /code
COPY requirements-dev.txt /code/
COPY requirements.txt /code/
RUN pip install -r requirements-dev.txt
COPY . /code/
