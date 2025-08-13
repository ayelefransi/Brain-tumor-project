FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for building and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.prod.txt ./
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy project
COPY . .

# Make entrypoint executable
RUN chmod +x /app/start.sh

EXPOSE 9000

CMD ["/app/start.sh"]