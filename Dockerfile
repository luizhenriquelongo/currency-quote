ARG EnvironmentVariable
# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"



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
EXPOSE 8000:8000

WORKDIR /app/backend
CMD poetry run gunicorn --bind :8000 --workers 3 config.wsgi:application
