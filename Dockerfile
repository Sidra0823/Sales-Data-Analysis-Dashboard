FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Set environment variables
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_LOGGER_LEVEL=info
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
