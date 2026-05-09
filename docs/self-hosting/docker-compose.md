# Docker Compose

The fastest way to self-host Bee Flow on a single host.

## 1. Clone the deploy repo

```bash
git clone https://github.com/Bee-Flow/beeflow.git
cd beeflow
cp .env.example .env
```

## 2. Edit `.env`

At minimum, set:

```bash
JWT_SECRET=<random 64+ char string>
DB_PASSWORD=<random>
ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY, MISTRAL_API_KEY
PUBLIC_URL=https://beeflow.example.com
```

See [Environment variables](env.md) for the full list.

## 3. Bring it up

```bash
docker compose up -d
```

This starts:

- `beeflow-server` on port `3101`
- `postgres` on port `5432` (internal)
- `redis` on port `6379` (internal)

## 4. Check it's running

```bash
curl http://localhost:3101/api/health
# {"status":"ok","version":"x.y.z","tier":"community"}
```

## 5. Point your frontend at it

If you're hosting the frontend yourself:

```bash
git clone https://github.com/Bee-Flow/hive.git
cd hive
npm install
VITE_API_URL=https://beeflow.example.com npm run build
# Serve dist/ behind any reverse proxy
```

## 6. Reverse proxy

Terminate TLS at your reverse proxy (Caddy, Nginx, Traefik) and forward to:

- `/` → frontend `dist/`
- `/api/`, `/auth/` → `http://beeflow-server:3101`

## Next

- [Apply a license key](../licensing/apply.md) to unlock paid features.
- [Connect Nextcloud](../connector/index.md) so users can sign in with their NC account.
