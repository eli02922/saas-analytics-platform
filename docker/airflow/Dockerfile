# Dockerfile for Apache Airflow
# Based on official Airflow image with custom additions

FROM apache/airflow:2.7.0-python3.11

# Switch to root to install additional packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements file from project root
COPY requirements.txt /tmp/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create necessary directories
RUN mkdir -p /opt/airflow/logs \
    && mkdir -p /opt/airflow/dags \
    && mkdir -p /opt/airflow/plugins

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow \
    PYTHONPATH=/opt/airflow/src

WORKDIR ${AIRFLOW_HOME}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
