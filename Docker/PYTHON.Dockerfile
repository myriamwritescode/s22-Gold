# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /C:\Users\Cameron\OneDrive\Desktop\s22-Gold\Docker
COPY requirements.txt /C:\Users\Cameron\OneDrive\Desktop\s22-Gold\Docker/
RUN pip install -r requirements.txt
COPY . /C:\Users\Cameron\OneDrive\Desktop\s22-Gold\Docker/