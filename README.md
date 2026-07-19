# Games Arcade

7 classic arcade games in a single HTML page — served by a lightweight Python HTTP server. Containerised for ARM64/AMD64 and ready for Raspberry Pi deployment.

**Games:** 2048, Tetris, Snake, Breakout, Memory Match, Tic-Tac-Toe, Pong

## Quick Start

```bash
pip install .   # or just: python3 server.py
# open http://localhost:8001
```

## Docker (local)

```bash
docker build -t games .
docker run -p 8001:8001 games
```

## Deploy via Docker + Cloudflare Tunnel

The image is multi-arch (linux/amd64, linux/arm64) and published to GHCR.

### Infrastructure

| Hostname | Device | Tunnels |
|----------|--------|---------|
| `rpi3.mollo.tech` | Raspberry Pi 3 | Base host |
| `games.mollo.tech` | Raspberry Pi 3 | Games arcade |
| `rpi5.mollo.tech` | Raspberry Pi 5 | Base host |
| `chef.mollo.tech` | Raspberry Pi 5 | Chef app |

Cloudflare Tunnels run as Docker containers (cloudflared sidecar pattern) on each Pi.

### 1. Deploy

SSH into the target Pi and run:

```bash
docker pull ghcr.io/atmollohan/games:latest
docker run -d --restart unless-stopped -p 8001:8001 ghcr.io/atmollohan/games:latest
```

Or use Docker Compose with the cloudflared sidecar (see `docker-compose.yml` in this repo):

```bash
export TUNNEL_TOKEN="your-cloudflare-tunnel-token"
docker compose up -d
```

### 2. Cloudflare Tunnel Setup

1. In Cloudflare Zero Trust dashboard, create a **tunnel**.
2. Copy the tunnel token.
3. Set it as the `TUNNEL_TOKEN` env var on the Pi.
4. Point the tunnel's public hostname to `http://localhost:8001`.

### 3. Tailscale (optional, private access)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

## CI/CD

Each push to `main` or a `v*.*.*` tag triggers a GitHub Action that builds and publishes multi-arch images to `ghcr.io/atmollohan/games`.

## Health Check

```bash
curl http://localhost:8001/health
# → {"status":"ok"}
```

## Environment Variables

| Variable | Default | Description     |
|----------|---------|-----------------|
| `PORT`   | `8001`  | Server port     |
| `HOST`   | `0.0.0.0` | Bind address  |

## License

MIT
