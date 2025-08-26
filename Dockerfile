FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir waitress

COPY . .

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/healthcheck')" || exit 1

CMD ["waitress-serve", "--host=0.0.0.0", "--port=80", "main:app"]