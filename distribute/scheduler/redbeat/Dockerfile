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
RUN pip install celery==5.3.6 celery-redbeat==2.2.0 redis==5.0.1 --ignore-installed

# Create a non-root user to run the container as.
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Make the directory for our container.
RUN mkdir -p /app/scripts

# Copy the needed code and files for our container.
COPY /app /app

# Download the script needed to wait for other containers and make it executable.
RUN curl -fO https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f17855a4dc21156cfe1694c31d7d1792e/wait-for-it.sh && mv /wait-for-it.sh  /app/scripts/wait-for-it.sh
RUN chmod +x /app/scripts/*.sh

# Grant the non-root user ownership of the app directory.
RUN chown -R appuser:appuser /app

# Set the python environment directory.
ENV PYTHONPATH=/..

# Run the container as the non-root user.
USER appuser
