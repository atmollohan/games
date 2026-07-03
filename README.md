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

## Deploy to RPi3 via Docker + Tailscale

The image is multi-arch (linux/amd64, linux/arm64) and published to GHCR.

### 1. Pull on the RPi

```bash
docker pull ghcr.io/atmollohan/games:latest
docker run -d --restart unless-stopped -p 8001:8001 ghcr.io/atmollohan/games:latest
```

### 2. Tailscale

```bash
# Install Tailscale on RPi (https://tailscale.com/download)
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# The RPi is now reachable at its Tailscale IP/name on port 8001
```

### 3. Docker Compose (with Cloudflare Tunnel)

Create `docker-compose.yml` on the RPi:

```yaml
services:
  games:
    image: ghcr.io/atmollohan/games:latest
    container_name: games
    restart: unless-stopped
    ports:
      - "8001:8001"

  tunnel:
    image: cloudflare/cloudflared:latest
    container_name: games-tunnel
    restart: unless-stopped
    command: tunnel --no-autoupdate run
    environment:
      - TUNNEL_TOKEN=${TUNNEL_TOKEN}
```

Set the tunnel token at runtime (never commit it):

```bash
export TUNNEL_TOKEN="your-cloudflare-tunnel-token"
docker compose up -d
```

### 4. Cloudflare Tunnel Setup

1. In Cloudflare Zero Trust dashboard, create a ** tunnel**.
2. Copy the tunnel token.
3. Set it as the `TUNNEL_TOKEN` env var on the RPi.
4. Point the tunnel's public hostname to `http://localhost:8001`.

Your app is now public through Cloudflare and private through Tailscale.

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
