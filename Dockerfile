FROM python:3.9
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y gcc python3-dev
RUN pip install -r requirements.txt


CMD exec gunicorn --bind 0.0.0.0:5000 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 2 main:app