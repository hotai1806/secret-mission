# Use a slim Python image
FROM python:3.13-slim


WORKDIR /app


# Copy dependency list first for better caching
COPY requirements.txt .

# Upgrade pip & install dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .



CMD ["python", "main.py"]