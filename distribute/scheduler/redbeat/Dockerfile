# Set the base docker image, we use slim from alpine because we care about performance.
FROM python:3.11.5-slim-bookworm

# Set working directory.
WORKDIR /..

# Set environment variables for python and OS.
ENV PYTHONFAULTHANDLER=1 \
    DEBIAN_FRONTEND=noninteractive \
    # Keeps Python from generating .pyc files in the container
    PYTHONDONTWRITEBYTECODE=1 \
    # Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Update the base image and install needed os packages.
RUN apt-get -y update --no-install-recommends \
    && apt-get -y install --no-install-recommends curl\
    && apt-get autoremove -y \
    && apt-get clean -y

# Enable again OS dialogs, after updating it.
ENV DEBIAN_FRONTEND=dialog

# Install needed packages for redbeat.
RUN pip install celery celery-redbeat redis --ignore-installed

# Make the directory for our container.
RUN mkdir -p /app/scripts

# Copy the needed code and files for our container.
COPY /app /app

# Download the script needed to wait for other containers and make it executable.
RUN curl -O https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && mv /wait-for-it.sh  /app/scripts/wait-for-it.sh
RUN chmod +x /app/scripts/*.sh

# Set the python environment directory.
ENV PYTHONPATH=/..
