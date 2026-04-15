# Use a slim Python image to reduce image size
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies if required by packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file explicitly
COPY requirements.txt .

# Install Python dependencies natively
RUN pip install --no-cache-dir -r requirements.txt

# =========================================================================
# CRITICAL LAYER: PRE-CACHE THE HUGGINGFACE MODEL
# If we do not download this at build time, the cloud platform (Render/etc)
# will halt your execution for ~30 seconds on every cold start while it 
# pulls the 320MB distilroberta network. Baking it into the image guarantees
# near instantaneous execution at runtime!
# =========================================================================
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', top_k=None)"

# Copy application source code into the container
COPY . .

# Ensure the static/ output folder exists and has proper permissions
RUN mkdir -p static && chmod 777 static

# Expose the standard Flask/Gunicorn port
EXPOSE 5000

# Use Gunicorn as the production WSGI server instead of pure Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "app:app"]
