# Base image
FROM python:3.10

ARG DJANGO_SECRET_KEY
ARG DATABASE_URL
ARG DJANGO_SETTINGS_MODULE


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
ENV DATABASE_URL=$DATABASE_URL
ENV PORT=$PORT

# Install Make
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*


    # Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

RUN export PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app/

# Install dependencies
RUN make build

# Expose the application port
EXPOSE $PORT

WORKDIR /app/backend
CMD poetry run gunicorn --workers 3 config.wsgi:application --log-level=info
