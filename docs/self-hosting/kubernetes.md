# Kubernetes

A Helm chart will be published at [Bee-Flow/helm](https://github.com/Bee-Flow/helm) once stable. Until then, the manifests below are a working starting point.

## Required workloads

| Workload | Replicas | Notes |
|----------|----------|-------|
| `beeflow-server` (Deployment) | 1+ | Stateless if Redis is configured |
| `postgres` (StatefulSet) | 1 | Or use a managed Postgres |
| `redis` (Deployment) | 1 | Or use managed Redis (e.g. ElastiCache) |
| `beeflow-frontend` (Deployment) | 1+ | Static files served by Nginx, or upload to S3/Cloudflare Pages |

## Required secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: beeflow-secrets
type: Opaque
stringData:
  JWT_SECRET: "<64+ random chars>"
  DB_PASSWORD: "<random>"
  ANTHROPIC_API_KEY: "sk-ant-..."
  # ...other model providers as needed
  # BEEFLOW_LICENSE_KEY: "eyJhbG..."   # optional
```

## ConfigMap

Non-secret configuration:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: beeflow-config
data:
  PUBLIC_URL: "https://beeflow.example.com"
  LOG_LEVEL: "info"
  DB_HOST: "postgres"
  DB_NAME: "beeflow"
  DB_USER: "beeflow"
  REDIS_URL: "redis://redis:6379"
  PORT: "3101"
```

## Server Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: beeflow-server
spec:
  replicas: 2
  selector:
    matchLabels: { app: beeflow-server }
  template:
    metadata:
      labels: { app: beeflow-server }
    spec:
      containers:
        - name: server
          image: ghcr.io/bee-flow/beeflow:latest
          ports: [{ containerPort: 3101 }]
          envFrom:
            - configMapRef: { name: beeflow-config }
            - secretRef: { name: beeflow-secrets }
          readinessProbe:
            httpGet: { path: /api/health, port: 3101 }
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /api/health, port: 3101 }
            initialDelaySeconds: 30
            periodSeconds: 30
          resources:
            requests: { cpu: 250m, memory: 512Mi }
            limits:   { cpu: 2,    memory: 2Gi }
---
apiVersion: v1
kind: Service
metadata: { name: beeflow-server }
spec:
  selector: { app: beeflow-server }
  ports: [{ port: 80, targetPort: 3101 }]
```

## Postgres StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata: { name: postgres }
spec:
  serviceName: postgres
  replicas: 1
  selector: { matchLabels: { app: postgres } }
  template:
    metadata: { labels: { app: postgres } }
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          env:
            - { name: POSTGRES_DB, value: beeflow }
            - { name: POSTGRES_USER, value: beeflow }
            - name: POSTGRES_PASSWORD
              valueFrom: { secretKeyRef: { name: beeflow-secrets, key: DB_PASSWORD } }
          ports: [{ containerPort: 5432 }]
          volumeMounts: [{ name: pg, mountPath: /var/lib/postgresql/data }]
  volumeClaimTemplates:
    - metadata: { name: pg }
      spec:
        accessModes: [ReadWriteOnce]
        resources: { requests: { storage: 50Gi } }
```

For production, prefer a managed Postgres (Neon, RDS, Cloud SQL, Supabase) — point `DB_HOST` at it and skip this StatefulSet.

## Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: beeflow
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
    nginx.ingress.kubernetes.io/proxy-buffering: "off"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
spec:
  tls:
    - hosts: [beeflow.example.com]
      secretName: beeflow-tls
  rules:
    - host: beeflow.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend: { service: { name: beeflow-server, port: { number: 80 } } }
          - path: /auth
            pathType: Prefix
            backend: { service: { name: beeflow-server, port: { number: 80 } } }
          - path: /webhook
            pathType: Prefix
            backend: { service: { name: beeflow-server, port: { number: 80 } } }
          - path: /
            pathType: Prefix
            backend: { service: { name: beeflow-frontend, port: { number: 80 } } }
```

The `proxy-buffering: "off"` annotation is **required** for SSE chat streaming.

## Scaling notes

- The server is stateless when Redis is configured. Increase `replicas`.
- Postgres is the bottleneck for write-heavy workloads (large KB ingestion, lots of automation runs). Tune `shared_buffers`, `effective_cache_size`, and consider a read replica for reporting.
- Redis is required for session state and rate limiting if you run >1 server replica.
- KB embedding ingestion is CPU-bound. Run the optional [`search-service`](https://github.com/Bee-Flow/search-service) on its own node for isolation.

## Helm chart status

A Helm chart (`bee-flow/beeflow`) is in progress. Track it at [https://github.com/Bee-Flow/helm](https://github.com/Bee-Flow/helm). PRs welcome.
