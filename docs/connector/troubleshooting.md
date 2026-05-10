# Troubleshooting

A reference of common problems with the connector. For each: symptom → cause → fix.

## Install hangs at "Deploying…"

| Symptom | Cause | Fix |
|---------|-------|-----|
| AppAPI deploy log shows `Image pull failed` | Daemon can't reach `ghcr.io` | `docker pull ghcr.io/bee-flow/connector:latest` from the host running the daemon. Whitelist `ghcr.io` + `pkg-containers.githubusercontent.com` in your egress firewall. |
| HaRP deploy returns `500 Internal Server Error` on `images/create` from a local registry | HaRP's Docker daemon doesn't trust HTTP registries | Add `{"insecure-registries":["registry:5000"]}` to the HaRP daemon's `/etc/docker/daemon.json` and restart, **or** switch to the `manual-install` daemon for local dev. |
| Deploy succeeds but heartbeat times out | Port 23000 already in use on the host | Stop the conflicting container, or change the AppAPI port mapping for the daemon. |
| Init reports `progress=0` and an error | Bootstrap failure (e.g. SaaS unreachable) | Check `docker logs nc_app_bee_flow` — see "Tenant key bootstrap" below. |

## "Heartbeat failed" in Nextcloud admin

The connector container is up but Nextcloud can't reach it. Run:

```bash
sudo -u www-data php occ app_api:app:heartbeat bee_flow
```

| Returns | Likely cause |
|---------|--------------|
| `{"status":"ok"}` from CLI but UI still red | Stale UI cache — refresh **Administration → AppAPI**. |
| `Connection refused` | Container not running. `docker ps \| grep bee_flow`, then `docker logs nc_app_bee_flow`. |
| `404 Not Found` | Wrong port mapping. Inspect `docker inspect nc_app_bee_flow` and confirm `23000` is published. |
| `Network unreachable` | NC and connector aren't on the same Docker network. Verify with `docker network inspect`. |

## Tenant key bootstrap fails

| Symptom in `docker logs nc_app_bee_flow` | Cause | Fix |
|------------------------------------------|-------|-----|
| `[Bootstrap] capabilities fetch timeout` | Connector can't reach NC | Check `NEXTCLOUD_URL` env. Ping it from inside the container: `docker exec nc_app_bee_flow curl $NEXTCLOUD_URL/status.php`. |
| `[Bootstrap] admin discovery: no admin found` | NC has no user in the `admin` group | Create one: `occ user:add --group admin alice`. |
| `[Bootstrap] SaaS responded 401` | Bee Flow service rejected the AppAPI signature | Check clocks (NTP) on both hosts. Verify `BEEFLOW_API_BASE_URL` is reachable. |
| `[Bootstrap] SaaS responded 409: instance already provisioned` | This NC was bootstrapped before; the tenant-key cache was lost | Recover the key from the SaaS admin UI (or contact support), set `BEEFLOW_TENANT_KEY=<key>` via `occ app_api:app:setenv`. |

The cache file is at `${APP_PERSISTENT_STORAGE}/tenant-key.json`. If it gets corrupted:

```bash
docker exec nc_app_bee_flow rm /data/tenant-key.json
docker exec nc_app_bee_flow kill -USR1 1   # triggers re-bootstrap, or just restart the container
```

## "Setup in progress" never goes away

Other users see this until the org admin completes the wizard. If you are the admin and still see it:

1. Reload the page (Cmd/Ctrl+Shift+R).
2. Check **Administration → AppAPI** — Bee Flow should show **Enabled**.
3. Check the connector logs: `docker logs nc_app_bee_flow --tail 100`.
4. Hit the SaaS health endpoint: `curl https://api.beeflow.ai/api/health` (or your self-hosted URL).

If the SaaS health is fine but the wizard still shows "Setup in progress", the tenant-key bootstrap probably ran but the SaaS didn't finish creating the org row. Restart the connector to force re-bootstrap.

## Nextcloud 33.0.0 — broken events listener

NC 33.0.0 ships AppAPI with a broken `EventsListenerController` that returns 500 to every `POST /ocs/v1.php/apps/app_api/api/v1/events_listener`. The connector probes the first call, detects this, and **skips the rest of the registrations** with a log line:

```
[Init] AppAPI 33.0.0 detected — events listener disabled
```

Effect: user/group changes in NC won't auto-sync to Bee Flow until you upgrade. The 6-hourly **NC Sync Backstop** job catches up — most teams won't notice. Upgrade to 33.0.1+ to restore real-time sync.

## HMAC clock-skew rejections

If Bee Flow service-side calls fail with:

```
401 Unauthorized: HMAC timestamp out of skew window
```

…the connector and the Bee Flow server have clocks more than 5 minutes apart. Fix:

```bash
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
```

To loosen the window temporarily (not recommended for prod):

```bash
sudo -u www-data php occ app_api:app:setenv bee_flow BEEFLOW_SIG_SKEW_SECONDS 600
```

## JWT TTL expired

The connector mints short-lived JWTs (default 300 s) for browser-side calls. If you see:

```
401 Unauthorized: token expired
```

…the SPA's token wasn't refreshed in time. The frontend usually auto-refreshes; if it doesn't, hard-reload the page. If it still fails, raise the TTL temporarily:

```bash
sudo -u www-data php occ app_api:app:setenv bee_flow BEEFLOW_JWT_TTL_SECONDS 600
```

(The short default is intentional — leaked-token containment.)

## Where to look

| Component | How to view logs |
|-----------|------------------|
| Connector container | `docker logs nc_app_bee_flow --tail 200 -f` |
| Nextcloud (AppAPI) | `tail -f data/nextcloud.log \| grep '"app":"app_api"'` |
| Nextcloud (Bee Flow specific) | `tail -f data/nextcloud.log \| grep bee_flow` |
| Bee Flow server (self-hosted) | `docker logs beeflow-server --tail 200 -f` |
| AppAPI deploy state | `occ app_api:app:list` and `occ app_api:app:status bee_flow` |
| Heartbeat | `occ app_api:app:heartbeat bee_flow` |

## Recovery commands cheat sheet

```bash
# Stop, remove, redeploy from clean
sudo -u www-data php occ app_api:app:unregister bee_flow
sudo -u www-data php occ app_api:app:register bee_flow \
  --info-xml https://raw.githubusercontent.com/Bee-Flow/connector/main/appinfo/info.xml

# Force a fresh tenant-key bootstrap
docker exec nc_app_bee_flow rm /data/tenant-key.json
docker restart nc_app_bee_flow

# Pin to a specific connector version
sudo -u www-data php occ app_api:app:update bee_flow --image-tag 0.2.0
```

## Where to ask

- Bug reports: [https://github.com/Bee-Flow/connector/issues](https://github.com/Bee-Flow/connector/issues)
- Security disclosure: [tomkooy@beeflow.nl](mailto:tomkooy@beeflow.nl)
- Commercial: [tomkooy@beeflow.nl](mailto:tomkooy@beeflow.nl)
