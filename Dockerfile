# Gebruik een lichte officiële Python runtime
FROM python:3.11-slim

# Werkmap instellen
WORKDIR /app

# Systeemafhankelijkheden en vereisten kopiëren
COPY requirements.txt .

# Installeer Python packages zonder cache
RUN pip install --no-cache-dir -r requirements.txt

# Applicatiecode kopiëren
COPY app.py .

# Standaard omgevingsvariabelen (kunnen overschreven worden via docker run -e)
ENV PORT=5000 \
    APP_NAME="Cloud Essentials Task Manager API" \
    ENVIRONMENT="AWS Academy Lab" \
    APP_VERSION="1.0.0" \
    PYTHONUNBUFFERED=1

# Documenteer poort
EXPOSE 5000

# Start de backend met Gunicorn voor een robuuste webserver
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]

