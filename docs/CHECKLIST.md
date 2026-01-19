# ✅ CHECKLIST DE CONFIGURACIÓN

Este documento te ayuda a verificar que todo está configurado correctamente.

---

## 🔧 Requisitos del Sistema

- [ ] Python 3.9+
- [ ] 4GB RAM mínimo (8GB recomendado)
- [ ] 2GB espacio libre (para modelo + deps)
- [ ] pip actualizado
- [ ] Conexión a internet (solo para primera instalación)

**Verificar Python:**
```bash
python --version  # Debe ser 3.9+
pip --version
```

---

## 📦 Instalación

- [ ] Directorio `modelo_entrenado_multiloss_portable/` existe
- [ ] Archivo `requirements.txt` presente
- [ ] Archivo `loader.py` presente
- [ ] Directorio `model/` con pesos (1.08GB)
- [ ] Archivo `api_wrapper.py` presente

**Verificar archivos:**
```bash
ls -lah  # Ver todos los archivos
du -sh model/  # Debe ser ~1.08GB
```

---

## 🐍 Ambiente Python

- [ ] Virtual environment creado (recomendado)
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] Sin errores en la instalación

**Verificar instalación:**
```bash
pip list | grep "torch\|sentence-transformers\|fastapi"
```

---

## 🧪 Prueba Básica del Modelo

- [ ] Ejecutado: `python loader.py ./model test`
- [ ] Test 1: Embedding OK
- [ ] Test 2: Similarity OK  
- [ ] Test 3: Search OK
- [ ] Test 4: Get Info OK

**Resultado esperado:**
```
✅ Test 1: Embedding - PASS
✅ Test 2: Similarity - PASS
✅ Test 3: Search - PASS
✅ Test 4: Get Info - PASS
```

---

## 🚀 Opción 1: Uso Directo en Python

- [ ] Ejecutado: `python examples/example_python.py`
- [ ] Todos los ejemplos pasaron
- [ ] Puedo importar: `from loader import load_model`
- [ ] Puedo crear modelo: `model = load_model("./model")`
- [ ] Puedo generar embedding: `embedding = model.encode("test")`

**Test rápido:**
```python
from loader import load_model
model = load_model("./model")
result = model.similarity("python", "java")
print(f"Similitud: {result}")  # Debe imprimir un número entre 0-1
```

---

## 🌐 Opción 2: API REST

### Servidor API

- [ ] Instaladas dependencias API: `fastapi`, `uvicorn`
- [ ] Ejecutado: `python api_wrapper.py --port 8000`
- [ ] Servidor inició sin errores
- [ ] Puerto 8000 está disponible

**Verificar puerto:**
```bash
netstat -an | grep 8000  # No debe mostrar nada si está libre
```

### Health Check

- [ ] `curl http://localhost:8000/health` retorna `{"status":"ok"}`
- [ ] `curl http://localhost:8000/info` retorna metadata del modelo

### Endpoints

- [ ] POST `/embed` - funciona
- [ ] POST `/similarity` - funciona
- [ ] POST `/search` - funciona
- [ ] POST `/cluster` - funciona

**Test rápido:**
```bash
curl -X POST http://localhost:8000/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["test"]}'
```

### Cliente API

- [ ] Instalado: `pip install requests`
- [ ] Ejecutado: `python examples/example_api_client.py` (en otra terminal)
- [ ] Todos los tests pasaron

---

## 🔌 Opción 3: Framework Web (Flask)

- [ ] Instalado: `pip install flask flask-cors`
- [ ] Ejecutado: `python examples/example_flask.py`
- [ ] Servidor Flask inició en `http://localhost:5000`
- [ ] Endpoints disponibles:
  - [ ] GET `/` - retorna info
  - [ ] POST `/api/search` - busca candidatos
  - [ ] POST `/api/similarity` - calcula similitud
  - [ ] GET `/api/cluster` - agrupa textos

**Test rápido:**
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python", "top_k": 3}'
```

---

## 🐳 Opción 4: Docker

- [ ] Instalado Docker
- [ ] Dockerfile presente
- [ ] Build exitoso: `docker build -t modelo-api:latest .`
- [ ] Container inicia: `docker run -p 8000:8000 modelo-api:latest`
- [ ] API accesible en `http://localhost:8000`

**Verificar Docker:**
```bash
docker --version
docker ps  # Ver containers activos
```

---

## 📚 Documentación

- [ ] README.md presente y legible
- [ ] INTEGRACION.md presente
- [ ] DEPLOYMENT.md presente
- [ ] MODEL_INFO.json presente
- [ ] examples/ directorio con ejemplos

**Verificar contenido:**
```bash
ls -lah *.md *.json
ls examples/
```

---

## ⚡ Rendimiento

- [ ] Embedding de 1 texto: < 100ms
- [ ] Embedding de 10 textos: < 500ms
- [ ] Similitud: < 100ms
- [ ] Búsqueda (100 items): < 10s
- [ ] Memoria: < 3GB en uso

**Benchmark:**
```bash
python -c "
from loader import load_model
import time
model = load_model('./model')
start = time.time()
for _ in range(10):
    model.encode('test')
print(f'Tiempo: {(time.time()-start)*1000/10:.2f}ms por embedding')
"
```

---

## 🔐 Seguridad (Producción)

- [ ] API key configurada (si aplica)
- [ ] SSL/TLS habilitado
- [ ] CORS configurado correctamente
- [ ] Rate limiting habilitado
- [ ] Logging configurado
- [ ] Backups configurados

**Verificar HTTPS:**
```bash
curl -I https://tu-servidor.com/health
```

---

## 📊 Monitoreo (Producción)

- [ ] Health checks configurados
- [ ] Logging iniciado
- [ ] Métricas recolectadas (si aplica)
- [ ] Alertas configuradas
- [ ] Dashboard disponible (si aplica)

**Ver logs:**
```bash
journalctl -u modelo-api -f  # Si usas systemd
docker logs modelo_api  # Si usas docker
```

---

## 🚨 Troubleshooting: Errores Comunes

### Error: ModuleNotFoundError

```
❌ ModuleNotFoundError: No module named 'torch'
```

**Solución:**
```bash
pip install torch sentence-transformers
```

### Error: Model not found

```
❌ FileNotFoundError: ./model/pytorch_model.bin
```

**Solución:**
```bash
ls -la model/  # Verificar que existan los archivos
du -sh model/  # Debe ser ~1.08GB
```

### Error: Port already in use

```
❌ OSError: [Errno 48] Address already in use
```

**Solución:**
```bash
# Opción 1: Liberar puerto
lsof -i :8000
kill -9 <PID>

# Opción 2: Usar puerto diferente
python api_wrapper.py --port 9000
```

### Error: Out of memory

```
❌ RuntimeError: CUDA out of memory
```

**Solución:**
```bash
# Forzar CPU
CUDA_VISIBLE_DEVICES=-1 python api_wrapper.py

# O en Python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

### Error: Slow performance

```
⚠️ Cada embedding tarda > 1 segundo
```

**Solución:**
```bash
# Verificar si usa GPU
python -c "import torch; print(torch.cuda.is_available())"

# Usar GPU si disponible
python api_wrapper.py --device cuda

# O hacer batch processing
model.encode(["text1", "text2", "text3"])  # Más rápido
```

---

## 📋 Antes de Ir a Producción

- [ ] ✅ Pasó todo el checklist anterior
- [ ] ✅ Testeado en desarrollo 2+ veces
- [ ] ✅ Documentación revisada
- [ ] ✅ Logs configurados
- [ ] ✅ Backups en lugar
- [ ] ✅ Rollback plan listo
- [ ] ✅ Equipo capacitado
- [ ] ✅ Monitoreo en lugar
- [ ] ✅ Alertas configuradas

---

## 📝 Notas Finales

### Después de Instalación

- [ ] Guardar esta copia del modelo en lugar seguro
- [ ] Anotar fecha de instalación
- [ ] Documentar cualquier customización
- [ ] Setup backups automáticos

### Mantenimiento Regular

- [ ] Revisar logs mensualmente
- [ ] Verificar uso de memoria
- [ ] Actualizar dependencias (cuando sea seguro)
- [ ] Hacer backups semanales

### En Caso de Problemas

1. Revisa logs: `journalctl -u modelo-api -f`
2. Reinstala dependencias: `pip install -r requirements.txt`
3. Verifica espacio: `df -h`
4. Reinicia servicio: `systemctl restart modelo-api`
5. Consulta documentación

---

## 🎯 Resumen: Estado del Deployment

| Componente | Estado | Verificado |
|-----------|--------|-----------|
| Python | ✅ | [ ] |
| Dependencias | ✅ | [ ] |
| Modelo | ✅ | [ ] |
| Loader | ✅ | [ ] |
| API | ✅ | [ ] |
| Ejemplos | ✅ | [ ] |
| Docker | ✅ | [ ] |
| Documentación | ✅ | [ ] |
| Seguridad | 🔄 | [ ] |
| Monitoreo | 🔄 | [ ] |

---

## 📞 Soporte

Si algo falla:

1. **Logs**: Revisa los logs del servicio
2. **Documentación**: Consulta README.md o INTEGRACION.md
3. **Ejemplos**: Ejecuta los ejemplos en `examples/`
4. **Health Check**: Verifica `curl http://localhost:8000/health`

---

*Última actualización: 8 de Enero, 2026*

**Estado actual:** ✅ **LISTO PARA PRODUCCIÓN** (después de completar checklist)
