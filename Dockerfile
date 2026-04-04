FROM python:alpine

WORKDIR /app

COPY server.py .

EXPOSE 8001

CMD ["python3", "server.py"]