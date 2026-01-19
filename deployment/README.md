# 🚀 DEPLOYMENT Y DESPLIEGUE

Guía completa para desplegar el modelo en producción.

## 📁 Contenido

```
deployment/
├── Dockerfile                        # Imagen Docker
├── docker-compose.yml                # Orquestación local
├── nginx.conf                        # Configuración Nginx
├── kubernetes/
│   └── deployment.yaml               # Manifesto Kubernetes
└── README.md                         # Este archivo
```

## 🐳 Opción 1: Docker Local

### Build

```bash
cd deployment
docker build -t recruitment-model:latest .
```

### Run

```bash
docker run -p 8000:8000 recruitment-model:latest
```

### Test

```bash
curl http://localhost:8000/health
```

## 🐘 Opción 2: Docker Compose

### Start

```bash
cd deployment
docker-compose up -d
```

### Servicios

- **API**: http://localhost:8000
- **Nginx**: http://localhost:80
- **Docs**: http://localhost:8000/docs

### Stop

```bash
docker-compose down
```

## ☸️ Opción 3: Kubernetes

### Prerequisites

```bash
kubectl version
helm version
```

### Deploy

```bash
cd deployment/kubernetes
kubectl apply -f deployment.yaml
```

### Verificar

```bash
kubectl get pods
kubectl get svc
```

### Port Forward

```bash
kubectl port-forward svc/recruitment-api 8000:8000
```

### Acceder

```
http://localhost:8000
```

## 📋 Opciones de Deployment

| Opción | Complejidad | Escalabilidad | Mejor Para |
|--------|-------------|---------------|-----------|
| Docker Local | ⭐ | Baja | Desarrollo |
| Docker Compose | ⭐⭐ | Media | Staging |
| Kubernetes | ⭐⭐⭐ | Alta | Producción |
| Cloud (AWS/GCP) | ⭐⭐⭐ | Muy Alta | Escala masiva |

## 🔧 Configuración

### Variables de Entorno

```bash
# .env
MODEL_PATH=./model
PORT=8000
DEVICE=cpu
LOG_LEVEL=info
```

### Performance

```bash
# Nginx (nginx.conf)
worker_processes auto;
keepalive_timeout 65;
```

```bash
# Docker Compose
services:
  api:
    environment:
      - WORKERS=4
      - THREADS_PER_WORKER=2
```

## 📊 Monitoring

### Logs

```bash
# Docker
docker logs recruitment-api

# Kubernetes
kubectl logs deployment/recruitment-api
```

### Health Check

```bash
curl http://localhost:8000/health
```

### Métricas

```bash
curl http://localhost:8000/metrics
```

## 🔐 Seguridad

### SSL/TLS

```bash
# Nginx reverse proxy con SSL
# Ver: nginx.conf
```

### Rate Limiting

```bash
# Docker Compose
RATE_LIMIT=100  # requests per minute
```

### Authentication

```bash
# Agregar API key
curl -H "X-API-Key: your-key" http://localhost:8000
```

## 📈 Escalabilidad

### Replicas

```bash
# Kubernetes
kubectl scale deployment recruitment-api --replicas=3
```

### Load Balancing

```bash
# Nginx (nginx.conf)
upstream api_backend {
    server api_1:8000;
    server api_2:8000;
    server api_3:8000;
}
```

## 🐛 Troubleshooting

### Puerto en uso

```bash
# Cambiar puerto
docker run -p 9000:8000 recruitment-model:latest
```

### Out of Memory

```bash
# Aumentar límites Docker
docker run -m 4g recruitment-model:latest
```

### Permisos de modelo

```bash
# Verificar acceso
docker run -v $(pwd)/model:/app/model:ro recruitment-model:latest
```

## 📝 Checklist Pre-Producción

- [ ] Tests locales pasan
- [ ] Evaluación de modelo OK
- [ ] Docker build exitoso
- [ ] Docker Compose funciona
- [ ] Kubernetes manifesto válido
- [ ] Variables de entorno configuradas
- [ ] SSL/TLS configurado
- [ ] Rate limiting establecido
- [ ] Logging habilitado
- [ ] Backups configurados
- [ ] Monitoreo activo
- [ ] Plan de rollback

## 🚀 Quick Start Production

```bash
# 1. Build
cd deployment
docker build -t recruitment-model:prod .

# 2. Tag
docker tag recruitment-model:prod your-registry.com/recruitment-model:prod

# 3. Push
docker push your-registry.com/recruitment-model:prod

# 4. Deploy en K8s
kubectl apply -f kubernetes/deployment.yaml

# 5. Verificar
kubectl get pods
kubectl get svc
```

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

**Tip:** Comienza con Docker Compose para staging, luego migra a Kubernetes para producción.
