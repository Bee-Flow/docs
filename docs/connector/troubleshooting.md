# Troubleshooting

## Install hangs at "Deploying…"

AppAPI's deploy log will show the cause. Most common:

- **Image pull failed** — your AppAPI deployment daemon can't reach `ghcr.io`. Check `docker pull ghcr.io/bee-flow/connector:latest` from the host running the daemon.
- **Port 23000 conflict** — another container is already on that port. Stop it or change the daemon port mapping.
- **Insecure local registry** (dev only) — if you're testing with a local registry over HTTP, add it to the Docker daemon's `insecure-registries`.

## "Heartbeat failed" in Nextcloud admin

The connector container is up but Nextcloud can't reach it on the AppAPI-assigned port. Run:

```bash
sudo -u www-data php occ app_api:app:heartbeat bee_flow
```

If the heartbeat returns `{"status":"ok"}` from the host but Nextcloud reports failure, you have a network-namespace mismatch — usually the AppAPI deployment daemon and the Nextcloud container aren't on the same Docker network.

## "Setup in progress" never goes away

Other users see this until the org admin completes the wizard. If you are the admin and still see it:

1. Reload the page (Cmd/Ctrl + Shift + R).
2. Check **Settings → Administration → AppAPI** — the connector should show **Enabled**.
3. Check the connector logs: `docker logs nc_app_bee_flow`.

## Logs

| Component | How to view |
|-----------|-------------|
| Connector container | `docker logs nc_app_bee_flow --tail 200 -f` |
| Nextcloud (AppAPI) | `tail -f data/nextcloud.log \| grep app_api` |
| Bee Flow service (self-hosted) | `docker logs beeflow-server --tail 200 -f` |

## Where to ask

- Bug reports: [github.com/Bee-Flow/connector/issues](https://github.com/Bee-Flow/connector/issues)
- Security: <tomkooy@beeflow.nl>
