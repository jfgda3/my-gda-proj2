FROM python:3.10

WORKDIR /app

# Caution: for WSL on local machine
# Set HTTPS Proxy
ENV HTTPS_PROXY=$https_proxy

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ingest_weather_data.py /app/

# Start Script
CMD ["python", "ingest_weather_data.py"]
