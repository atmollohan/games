# Roadmap

## Phase 1 — Docker & CI/CD (Done)
- [x] Lightweight Dockerfile (Alpine-based)
- [x] Multi-arch build (amd64 + arm64) for RPi3
- [x] .dockerignore for smaller builds
- [x] Multi-platform build via GitHub Actions (PR checks, build, deploy, release)
- [x] Docker Compose with cloudflared sidecar
- [x] Dependabot for Docker + Actions updates

## Phase 2 — Server-Side Game Engine
- [x] `games/` package with chess, checkers, tictactoe engines
- [x] Minimax AI (depth 2 chess, depth 4 checkers) on server
- [x] Pure function core + GameState container for testability
- [x] HTTP JSON API: init, state, move/action endpoints
- [x] Client-side renderers consume API (no local game logic)
- [ ] Move Tetris, Snake, 2048 to server
- [ ] Real-time games via WebSocket (Pong, Breakout, Flappy Bird)
- [ ] Tests for all game engines

## Phase 3 — Frontend Architecture
- [x] Split monolithic index.html → static/ directory
- [x] Per-game JS renderers in static/js/
- [x] Mobile detection (user-agent) with game filtering
- [ ] Touch controls for keyboard-dependent games
- [ ] Sound effects (Web Audio API)

## Phase 4 — Deployment
- [x] Deploy to RPi3 via Docker (Tailscale network)
- [x] Cloudflare Tunnel (cloudflared) for public ingress
- [ ] Graceful shutdown / signal handling
- [x] docker restart policy for reliability

## Phase 5 — Quality of Life
- [ ] Logging middleware (access logs, optional structured logging)
- [ ] Readiness probe (`GET /health`)
- [ ] Prometheus metrics endpoint (optional)
- [ ] Game stats / leaderboard (server-side)
- [ ] Multi-player over WebSocket
