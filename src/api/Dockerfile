# ── Flask API Container ──────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Cache-bust arg — increment to force fresh COPY . . layer
ARG CACHE_BUST=15

# System dependencies for scikit-learn / scipy
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application source
COPY . .

# SQLite database lives in /data (mounted as a volume in production)
RUN mkdir -p /data
ENV DB_PATH=/data/student_loan_data.db

EXPOSE 5000

# Use gunicorn for production; 2 workers suitable for CPU-bound ML tasks
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "300", "app:app"]
