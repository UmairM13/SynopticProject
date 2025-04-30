FROM python:3.11.12-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc g++ gfortran libpq-dev libffi-dev libssl-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Ensure Python can find your module
ENV PYTHONPATH=/app

# Copy files
COPY .env .env
COPY requirements.txt requirements.txt
COPY recommendation_engine ./recommendation_engine

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "recommendation_engine.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
