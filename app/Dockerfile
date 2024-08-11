FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set work directory
WORKDIR /home/app/web

# Install psycopg2, Pillow, and other dependencies
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev \
musl-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev \
tk-dev tcl-dev libxml2-dev libxslt-dev libffi-dev openssl-dev curl

# Copy project files
COPY . .

# Conditionally copy .env file if it exists
COPY .env .

# Install pip and dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy entrypoint.sh and project files
COPY entrypoint.sh .
# RUN chmod +x entrypoint.sh


# Ensure permissions
RUN chmod -R 755 /home/app/web

# Run migrations and collect static files
RUN python manage.py migrate && \
    python manage.py collectstatic --noinput

# Start Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
