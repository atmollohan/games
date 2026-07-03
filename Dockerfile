FROM python:3.14-alpine
WORKDIR /app
COPY server.py .
COPY games/ games/
COPY static/ static/
RUN adduser -D -h /app appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8001/health || exit 1
CMD ["python3", "server.py"]
