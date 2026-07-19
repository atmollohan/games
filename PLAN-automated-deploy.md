# Automated Deployment via Tailscale

## Current State

| Workflow | Trigger | Target | Status |
|----------|---------|--------|--------|
| `build.yml` | Push to `main` | GHCR (multi-arch) | Working |
| `deploy.yml` | Manual only | rpi3 only | Working but limited |
| `release.yml` | Manual only | rpi3 only | Working but limited |
| `pr-checks.yml` | PRs | N/A | Working |

Manual deploy via Tailscale SSH + docker commands is sufficient during game development.

## Gaps

1. **No auto-deploy on push to main** — `build.yml` pushes images but nothing pulls them onto the Pi
2. **Single-Pi targeting** — Both `deploy.yml` and `release.yml` hardcode `PI_HOSTNAME: rpi3`
3. **Duplicated deploy logic** — Deploy + health check steps are copy-pasted between workflows
4. **`TUNNEL_TOKEN` not wired up** — Inline compose references `${TUNNEL_TOKEN}` but it's never exported on the Pi during deploy
5. **No rollback path** — Failed deploys require manual intervention

## Plan

### Phase 1: Reusable deploy workflow

Extract Tailscale SSH + docker compose + health check into `deploy-reusable.yml`.

Inputs: `image_tag`, `pi_hostname`, `pi_user`, `app_dir`.

Both `deploy.yml` and `release.yml` call this instead of duplicating logic.

### Phase 2: Multi-Pi support

- Matrix or input to select target Pi(s)
- Per-Pi config: hostname, user, app_dir, tunnel token secret
- Deploy to rpi3, rpi5, or both independently

### Phase 3: Auto-deploy on push to main

Chain deploy after `build.yml` pushes `:latest`. Either as a job in `build.yml` or a separate `deploy-on-push.yml`.

### Phase 4: Tunnel token handling

- Store `TUNNEL_TOKEN` as a GitHub secret per Pi (`TUNNEL_TOKEN_RPI3`, `TUNNEL_TOKEN_RPI5`)
- Pass through to Pi during deploy so compose works end-to-end
