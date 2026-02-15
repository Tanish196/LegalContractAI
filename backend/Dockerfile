# Build stage
FROM python:3.11-slim as builder

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Create virtual environment and install dependencies with uv
RUN uv pip install --system -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Install uv in runtime for any future package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy virtual environment from builder (optional - for optimization)
# Or copy entire app and reinstall (simpler approach below)

# Copy application code
COPY . .

# Install dependencies again in runtime
RUN uv pip install --system -r requirements.txt

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
