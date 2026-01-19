# 🚀 GUÍA DE DEPLOYMENT

Esta guía explica cómo desplegar el modelo en diferentes entornos.

## 📋 Tabla de Contenidos

1. [Desarrollo Local](#desarrollo-local)
2. [Producción en Servidor](#producción-en-servidor)
3. [Docker](#docker)
4. [Cloud](#cloud)
5. [Monitoreo](#monitoreo)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Desarrollo Local

### Instalación Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Probar el modelo
python loader.py ./model test

# 3. Iniciar la API
python api_wrapper.py --port 8000

# 4. En otra terminal, probar
python examples/example_api_client.py
```

### Desarrollo con Reload Automático

```bash
# Con reload automático (para desarrollo)
python api_wrapper.py --reload --port 8000

# Con logging detallado
python api_wrapper.py --port 8000 --debug
```

---

## 🌐 Producción en Servidor

### Instalación en Ubuntu/Debian

```bash
# 1. Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# 2. Instalar Python 3.11
sudo apt-get install python3.11 python3.11-venv

# 3. Crear directorio de aplicación
sudo mkdir -p /opt/modelo-api
sudo chown $USER:$USER /opt/modelo-api

# 4. Copiar archivos
cp -r . /opt/modelo-api/
cd /opt/modelo-api

# 5. Crear virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 6. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 7. Probar
python api_wrapper.py --port 8000
```

### Usar Gunicorn (WSGI)

```bash
# Instalar gunicorn
pip install gunicorn

# Crear archivo app.py
cat > app.py << 'EOF'
from api_wrapper import app

if __name__ == "__main__":
    app.run()
EOF

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Usar Systemd (Recomendado)

```bash
# Crear servicio systemd
sudo tee /etc/systemd/system/modelo-api.service > /dev/null << 'EOF'
[Unit]
Description=Modelo API Service
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=/opt/modelo-api
Environment="PATH=/opt/modelo-api/venv/bin"
ExecStart=/opt/modelo-api/venv/bin/python api_wrapper.py --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd
sudo systemctl daemon-reload

# Iniciar servicio
sudo systemctl start modelo-api

# Habilitar al arranque
sudo systemctl enable modelo-api

# Ver status
sudo systemctl status modelo-api

# Ver logs
sudo journalctl -u modelo-api -f
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/modelo
upstream modelo_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.ejemplo.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://modelo_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL con Certbot

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot certonly --nginx -d api.ejemplo.com

# Auto-renovar
sudo systemctl enable certbot.timer
```

---

## 🐳 Docker

### Build y Run

```bash
# Build imagen
docker build -t modelo-api:latest .

# Run contenedor
docker run -p 8000:8000 modelo-api:latest

# Run con GPU
docker run --gpus all -p 8000:8000 modelo-api:latest

# Run con environment variables
docker run -e TORCH_DEVICE=cuda -p 8000:8000 modelo-api:latest
```

### Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f modelo-api

# Detener
docker-compose down
```

### Registry (Docker Hub)

```bash
# Login
docker login

# Tag imagen
docker tag modelo-api:latest usuario/modelo-api:latest

# Push
docker push usuario/modelo-api:latest

# Pull
docker pull usuario/modelo-api:latest
```

---

## ☁️ Cloud

### Heroku

```bash
# 1. Instalar Heroku CLI
curl https://cli.herokuapp.com/install.sh | sh

# 2. Login
heroku login

# 3. Crear app
heroku create mi-modelo-api

# 4. Crear Procfile
echo "web: python api_wrapper.py --port \$PORT --host 0.0.0.0" > Procfile

# 5. Deploy
git push heroku main

# 6. Ver logs
heroku logs --tail
```

### AWS Lambda + API Gateway

```bash
# Usar SAM (Serverless Application Model)
sam init

# Template para Lambda
# template.yaml
Resources:
  ModeloApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: api_wrapper.lambda_handler
      Runtime: python3.11
      MemorySize: 3008
      Timeout: 60
```

### Google Cloud Run

```bash
# Push a Container Registry
docker tag modelo-api gcr.io/mi-proyecto/modelo-api
docker push gcr.io/mi-proyecto/modelo-api

# Deploy a Cloud Run
gcloud run deploy modelo-api \
  --image gcr.io/mi-proyecto/modelo-api \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --timeout 3600
```

### Azure Container Instances

```bash
# Push a Container Registry
az acr build --registry miregistro --image modelo-api:latest .

# Deploy
az container create \
  --resource-group mi-grupo \
  --name modelo-api \
  --image miregistro.azurecr.io/modelo-api:latest \
  --cpu 4 \
  --memory 8 \
  --port 8000
```

---

## 📊 Monitoreo

### Health Checks

```bash
# Simple
curl http://localhost:8000/health

# Con timeout
curl --max-time 5 http://localhost:8000/health

# Script de monitoreo
#!/bin/bash
while true; do
  status=$(curl -s http://localhost:8000/health | jq -r '.status')
  echo "$(date): Status = $status"
  sleep 30
done
```

### Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'modelo-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

```bash
# Docker
docker run -d -p 3000:3000 grafana/grafana

# Acceder
# http://localhost:3000
# Usuario: admin / Contraseña: admin
```

### Logging

```bash
# Ver logs en tiempo real
tail -f /var/log/modelo-api.log

# Buscar errores
grep ERROR /var/log/modelo-api.log

# Con journalctl
journalctl -u modelo-api -f

# Analizar logs
cat /var/log/modelo-api.log | jq .
```

---

## 🔧 Troubleshooting

### Puerto en uso

```bash
# Encontrar proceso
lsof -i :8000

# Matar proceso
kill -9 <PID>

# Usar puerto diferente
python api_wrapper.py --port 9000
```

### Memoria insuficiente

```bash
# Monitorear memoria
watch -n 1 'ps aux | grep api_wrapper'

# Usar swap
sudo dd if=/dev/zero of=/swapfile bs=1G count=4
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Limitar memoria (Docker)
docker run -m 4g modelo-api:latest
```

### GPU no detectada

```bash
# Verificar CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Forzar CPU
CUDA_VISIBLE_DEVICES=-1 python api_wrapper.py

# Verificar docker con GPU
docker run --gpus all --rm nvidia/cuda:11.8.0-runtime nvidia-smi
```

### Modelo corrupto

```bash
# Verificar integridad
python -c "from loader import load_model; model = load_model('./model')"

# Redownload si es necesario
# (instrucciones específicas según origen)
```

### SSL Certificate Issues

```bash
# Verificar certificado
openssl s_client -connect api.ejemplo.com:443

# Renovar certificado
sudo certbot renew --force-renewal
```

---

## ⚡ Optimizaciones

### Performance Tuning

```bash
# Usar múltiples workers (Gunicorn)
gunicorn -w 8 -b 0.0.0.0:8000 app:app

# Aumentar file descriptors
ulimit -n 65536

# TCP tuning
sysctl -w net.core.somaxconn=65536
sysctl -w net.ipv4.tcp_max_syn_backlog=65536
```

### Caching

```bash
# Redis para cache
docker run -d -p 6379:6379 redis:latest

# En aplicación
import redis
cache = redis.Redis(host='localhost', port=6379)
```

### Load Balancing

```nginx
upstream modelo_cluster {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

---

## 📈 Escalabilidad

### Horizontal Scaling

```bash
# Múltiples instancias
for i in {1..3}; do
  python api_wrapper.py --port $((8000 + i)) &
done

# Load balancer
nginx (upstream with round-robin)
```

### Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: modelo-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: modelo-api
  template:
    metadata:
      labels:
        app: modelo-api
    spec:
      containers:
      - name: modelo-api
        image: modelo-api:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
```

---

## 🔐 Seguridad

### API Key Authentication

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/api/search")
async def search(query: str, api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    # ... rest of logic
```

### Rate Limiting

```bash
# Con Nginx (ya en nginx.conf)
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req zone=api_limit burst=20 nodelay;
```

### HTTPS/TLS

```bash
# Ya cubierto con Certbot arriba
sudo certbot certonly --nginx -d api.ejemplo.com
```

---

## 📊 Checklist de Deployment

- [ ] Instalar dependencias
- [ ] Probar modelo localmente
- [ ] Configurar base de datos (si aplica)
- [ ] Configurar logging
- [ ] Configurar monitoreo
- [ ] Configurar backups
- [ ] Configurar alertas
- [ ] SSL/TLS
- [ ] Rate limiting
- [ ] API authentication
- [ ] Database replication (si aplica)
- [ ] Load balancer
- [ ] Auto-scaling
- [ ] Disaster recovery plan

---

*Última actualización: 8 de Enero, 2026*
