FROM python:3.8.6-slim

RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install g++ -y

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501
