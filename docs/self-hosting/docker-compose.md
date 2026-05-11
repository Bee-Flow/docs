---
title: Docker Compose
---

# Docker Compose

The fastest way to self-host Bee Flow on a single host. Production-ready for small/mid orgs.

## 1. Clone and configure

```bash
git clone https://github.com/Bee-Flow/beeflow.git
cd beeflow
cp .env.example .env
```

## 2. Edit `.env`

Minimum required:

```bash
# Core
PUBLIC_URL=https://beeflow.example.com
JWT_SECRET=<random 64+ char string>      # openssl rand -hex 32
LOG_LEVEL=info

# Database
DB_PASSWORD=<random>

# At least one model provider:
ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
# MISTRAL_API_KEY=...
# AZURE_OPENAI_ENDPOINT=https://...
# AZURE_OPENAI_KEY=...
```

See [Environment variables](env.md) for the full reference (~80 vars).

## Three databases, not one {#three-databases-not-one}

The shipped `docker-compose.yml` creates **three** Postgres databases on the same instance:

| Database | What it stores | Used by |
|---|---|---|
| `beeflow_core` | Users, agents, conversations, KBs, audit log, settings — the bulk of state | Main server (`DB_NAME`) |
| `beeflow_tasks` | Project / reminder / aiTasks rows for the productivity layer | Main server (`DATABASE_URL` override on the `tasks` routes) |
| `monitoring_db` | Long-tail metrics + ticket-assistant analytics | Main server (`MONITORING_DATABASE_URL`) |

All three live in the same Postgres instance; the `init-multi-db.sh` script at the repo root creates the auxiliary databases on first start. Override the names via `DB_NAME=...` and the matching `DATABASE_URL=` / `MONITORING_DATABASE_URL=` env vars if you'd rather use a single DB.

## 3. The compose file

The shipped `docker-compose.yml` looks roughly like this — you can use it as-is or adapt:

```yaml
services:
  beeflow-server:
    image: ghcr.io/bee-flow/beeflow:latest
    restart: unless-stopped
    env_file: .env
    environment:
      - DB_HOST=postgres
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres: { condition: service_healthy }
      redis: { condition: service_started }
    ports:
      - "127.0.0.1:3101:3101"
    volumes:
      - beeflow_data:/data

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME:-beeflow_core}
      POSTGRES_USER: beeflow
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      # The init script creates the auxiliary databases below.
      POSTGRES_MULTIPLE_DATABASES: beeflow_tasks,monitoring_db
    volumes:
      - pg_data:/var/lib/postgresql/data
      - ./init-multi-db.sh:/docker-entrypoint-initdb.d/init-multi-db.sh:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U beeflow"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis_data:/data

volumes:
  beeflow_data:
  pg_data:
  redis_data:
```

## 4. Start

```bash
docker compose up -d
```

Wait ~10 s, then:

```bash
curl http://127.0.0.1:3101/api/health
# {"status":"ok","version":"x.y.z","tier":"community"}
```

## 5. Reverse proxy + TLS

Pick one — your reverse proxy terminates TLS and forwards `/api/`, `/auth/`, and the SPA `/`.

### Caddy (simplest)

```caddyfile
beeflow.example.com {
    handle /api/* { reverse_proxy 127.0.0.1:3101 }
    handle /auth/* { reverse_proxy 127.0.0.1:3101 }
    handle /webhook/* { reverse_proxy 127.0.0.1:3101 }
    handle { root * /var/www/beeflow-frontend; file_server; try_files {path} /index.html }
}
```

### Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name beeflow.example.com;
    ssl_certificate /etc/letsencrypt/live/.../fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/.../privkey.pem;

    root /var/www/beeflow-frontend;
    index index.html;

    location / { try_files $uri /index.html; }

    location /api/ {
        proxy_pass http://127.0.0.1:3101;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;          # SSE
        proxy_read_timeout 600s;
    }
    location /auth/   { proxy_pass http://127.0.0.1:3101; }
    location /webhook/{ proxy_pass http://127.0.0.1:3101; }
}
```

The `proxy_buffering off` + `proxy_read_timeout` lines are required for chat streaming to work.

### Traefik (Docker Compose labels)

```yaml
services:
  beeflow-server:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.beeflow.rule=Host(`beeflow.example.com`) && (PathPrefix(`/api`) || PathPrefix(`/auth`) || PathPrefix(`/webhook`))"
      - "traefik.http.routers.beeflow.tls.certresolver=letsencrypt"
      - "traefik.http.services.beeflow.loadbalancer.server.port=3101"
      - "traefik.http.services.beeflow.loadbalancer.server.scheme=http"
```

## 6. Build and serve the frontend

```bash
git clone https://github.com/Bee-Flow/hive.git
cd hive
npm install
VITE_API_URL=https://beeflow.example.com npm run build
sudo cp -r dist/* /var/www/beeflow-frontend/
```

Or pull the prebuilt npm package:

```bash
mkdir /var/www/beeflow-frontend
cd /tmp && npm pack @beeflow/frontend
tar -xzf beeflow-frontend-*.tgz
cp -r package/dist/* /var/www/beeflow-frontend/
```

## 7. Apply a licence key (optional)

For premium features, paste your JWT licence key in **Settings → Organisation → License & usage**. See [Applying a licence key](../licensing/apply.md).

## 8. Connect Nextcloud (optional)

If you also run Nextcloud, install the Bee Flow connector:

```bash
sudo -u www-data php occ app_api:app:register bee_flow \
  --info-xml https://raw.githubusercontent.com/Bee-Flow/connector/main/appinfo/info.xml \
  --env BEEFLOW_API_BASE_URL=https://beeflow.example.com
```

The connector talks to your self-hosted server instead of the hosted SaaS.

## Backups

Everything durable lives in Postgres. Back up daily with `pg_dump`:

```bash
docker exec -t $(docker compose ps -q postgres) \
  pg_dump -U beeflow -d beeflow -Fc > /backups/beeflow-$(date +%F).dump
```

Restore:

```bash
cat backup.dump | docker exec -i $(docker compose ps -q postgres) \
  pg_restore -U beeflow -d beeflow --clean --if-exists
```

The `beeflow_data` volume holds short-lived state only — losing it is recoverable from Postgres on restart.

## Swap Postgres for managed

Bee Flow needs Postgres 16+ with `pgvector` if you want vector KBs. Tested managed providers:

| Provider | Notes |
|----------|-------|
| Neon | ✅ — pgvector built-in. |
| Supabase | ✅ — pgvector built-in. |
| AWS RDS | ✅ — install `pgvector` extension (RDS supports it). |
| Google Cloud SQL | ✅ — install `pgvector` extension. |
| Heroku Postgres | ⚠️ — works for non-vector KBs only (no pgvector). |

Point `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` at the managed instance and remove the `postgres` service from the compose file.

## Restart and update

```bash
# Restart server only
docker compose restart beeflow-server

# Pull new image and restart
docker compose pull beeflow-server
docker compose up -d beeflow-server

# View logs
docker compose logs -f beeflow-server
```

[More on upgrades →](upgrades.md)

## Production hardening checklist

- [ ] `JWT_SECRET` set to a fresh 64+ char random string
- [ ] `DB_PASSWORD` set; Postgres not exposed publicly
- [ ] HTTPS in front of `:3101` (the server speaks plain HTTP internally)
- [ ] OAuth redirect URIs registered with each provider you enable
- [ ] Daily `pg_dump` running and tested-restored at least once
- [ ] At least one model provider key set
- [ ] `LOG_LEVEL=info` (not `debug`) in production
- [ ] Rate limit at the reverse proxy (e.g. Caddy `request_body max_size 10MB`, Nginx `limit_req_zone`)
- [ ] Audit log shipped off-host (Loki / ELK / Splunk) — see [Reference → Telemetry](../reference/telemetry.md)
