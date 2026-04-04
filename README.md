# Games App

Lightweight HTTP server for hosting simple HTML games.

## Run Locally

```bash
python3 server.py
```

Then open http://localhost:8001

## Run with Docker

```bash
docker build -t games .
docker run -p 8001:8001 games
```

## Raspberry Pi

Build for ARM:
```bash
docker build -t games .
docker run -p 8001:8001 games
```

The Alpine-based image works well on Raspberry Pi (ARM).

## Port

Default port: 8001