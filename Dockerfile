FROM python:3.8.2-slim
ENV PYTHONBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code/.
