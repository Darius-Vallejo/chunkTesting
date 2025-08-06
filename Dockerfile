FROM python:3.11-slim

WORKDIR /app

COPY chunked_server.py .

EXPOSE 8080

CMD ["python", "chunked_server.py"]
