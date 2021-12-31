FROM python:3.10-rc-buster
ENV PYTHONUNBUFFERED 1

# Install packages
#   * node: To run the build scripts.
RUN apt update \
    && apt upgrade -y \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt install -y nodejs \
    && apt install -y daphne \
    && mkdir -p /app

# Webp Support
RUN apt install libwebp-dev -y

WORKDIR /app/

# Install the python packages seperately as it is less likely they will need
# updating whereas it is likely the npm packages may be updated in the future.
COPY ./requirements.txt ./requirements.txt
# Temp removal - was causing issues.
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install && npm audit fix
COPY . .

RUN npx browserslist@latest --update-db
RUN npm run build
