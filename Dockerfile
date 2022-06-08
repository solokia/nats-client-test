FROM python:3.9
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y gcc python3-dev
RUN pip install -r requirements.txt


CMD python main.py