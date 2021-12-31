FROM python:3.10-rc-buster
ENV PYTHONUNBUFFERED 1

# Install packages
#   * node: To run the build scripts.
RUN apt update \
    && apt upgrade -y \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt install -y nodejs \
    && apt install -y daphne \
    && apt install -y vim \
    && mkdir -p /app

# Webp Support
RUN apt install libwebp-dev -y

WORKDIR /app

COPY . .

RUN ls -lrta
RUN pip install -r requirements.txt
