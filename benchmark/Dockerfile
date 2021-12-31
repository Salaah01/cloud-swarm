FROM python:3.9.9-bullseye
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt upgrade -y \
    && mkdir -p /app

# Setup AWS
COPY ./.aws /root/.aws

# Setup SSH
COPY ./.ssh /root/.ssh

WORKDIR /app/

# Install Python packages
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .