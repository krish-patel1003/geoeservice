FROM python:3.11

ARG SECRET_NAME

ARG SECRET_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG S3_ACCESS_KEY_ID
ARG S3_SECRET_ACCESS_KEY

ENV SECRET_NAME=$SECRET_NAME
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV S3_ACCESS_KEY_ID=$S3_ACCESS_KEY_ID
ENV S3_SECRET_ACCESS_KEY=$S3_SECRET_ACCESS_KEY

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libffi-dev libcairo2-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install\
    && apt-get install -y libpq-dev libgl1 libgl1-mesa-glx libglib2.0-0 -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
EXPOSE 8000

WORKDIR /app/geoservice
CMD ["gunicorn", "-w", "3", "-b", ":8000", "geoservice.wsgi:application"]
