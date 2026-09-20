FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data /app/logs && chown -R appuser:appuser /app
USER appuser
CMD ["python", "main.py"]
