FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory
RUN mkdir -p /home/app/web
WORKDIR /home/app/web

# Install psycopg2 & pillow dependencies
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    openssl-dev \
    curl

# Conditionally copy .env file if it exists
COPY .env .

# Install pip and dependencies
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy entrypoint.sh and project files
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# start gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]