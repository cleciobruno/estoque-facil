FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt gunicorn

COPY . .
WORKDIR /app/backend

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:criar_app()"]