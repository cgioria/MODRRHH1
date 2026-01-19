# 🔄 CAMBIAR ENDPOINT DE GIT - GUÍA COMPLETA

## 📍 Ver endpoint actual

```bash
# Ver la URL remota actual
git remote -v

# Salida esperada:
# origin  https://github.com/usuario/repo.git (fetch)
# origin  https://github.com/usuario/repo.git (push)
```

---

## ✅ OPCIÓN 1: Cambiar URL remota (MÁS SIMPLE)

### Paso 1: Cambiar la URL
```bash
git remote set-url origin <NUEVA_URL>
```

### Ejemplos:

**Cambiar a GitHub:**
```bash
git remote set-url origin https://github.com/nuevo-usuario/nuevo-repo.git
```

**Cambiar a GitLab:**
```bash
git remote set-url origin https://gitlab.com/nuevo-usuario/nuevo-repo.git
```

**Cambiar a Bitbucket:**
```bash
git remote set-url origin https://bitbucket.org/nuevo-usuario/nuevo-repo.git
```

**Cambiar a repositorio local:**
```bash
git remote set-url origin /ruta/local/nuevo-repo.git
```

**Cambiar a SSH:**
```bash
git remote set-url origin git@github.com:nuevo-usuario/nuevo-repo.git
```

### Paso 2: Verificar que cambió
```bash
git remote -v
# Debe mostrar la nueva URL
```

### Paso 3: Push a nuevo repositorio
```bash
git push -u origin main
# O si tu rama principal se llama diferente:
git push -u origin master
```

---

## ✅ OPCIÓN 2: Cambiar nombre remoto

Si quieres cambiar de `origin` a otro nombre:

```bash
# Renombrar remote
git remote rename origin upstream

# Crear nuevo origin
git remote add origin <NUEVA_URL>

# Verificar
git remote -v
```

---

## ✅ OPCIÓN 3: Cambiar a múltiples remotes

Si quieres mantener el anterior y agregar uno nuevo:

```bash
# Ver actuales
git remote -v

# Renombrar el actual
git remote rename origin upstream

# Agregar nuevo origin
git remote add origin <NUEVA_URL>

# Verificar
git remote -v
```

---

## 📋 GUÍA PASO A PASO COMPLETA

### Para tu proyecto actual:

#### Paso 1: Verificar estado actual
```bash
cd c:\Code\Vectorizacion\recruitment_automation\modelo_entrenado_multiloss_portable

git remote -v
```

#### Paso 2: Cambiar URL (elige tu opción)

**Opción A: GitHub**
```bash
git remote set-url origin https://github.com/TU_USUARIO/recruitment-model.git
```

**Opción B: GitLab**
```bash
git remote set-url origin https://gitlab.com/TU_USUARIO/recruitment-model.git
```

**Opción C: Bitbucket**
```bash
git remote set-url origin https://bitbucket.org/TU_USUARIO/recruitment-model.git
```

**Opción D: Azure Repos**
```bash
git remote set-url origin https://dev.azure.com/TU_USUARIO/TU_PROYECTO/_git/recruitment-model
```

**Opción E: Repositorio privado local**
```bash
git remote set-url origin C:\ruta\a\nuevo\repo.git
```

#### Paso 3: Verificar cambio
```bash
git remote -v
```

#### Paso 4: Hacer push inicial
```bash
# Hacer push de todas las ramas
git push -u origin --all

# O solo la rama actual
git push -u origin main
```

---

## 🔐 CON AUTENTICACIÓN (SSH vs HTTPS)

### Cambiar a SSH (MÁS SEGURO)

```bash
# Ver configuración actual
git remote -v

# Cambiar a SSH
git remote set-url origin git@github.com:TU_USUARIO/recruitment-model.git

# Verificar
git remote -v
```

### Cambiar a HTTPS (CON TOKEN)

```bash
# Cambiar a HTTPS con token
git remote set-url origin https://TU_TOKEN@github.com/TU_USUARIO/recruitment-model.git

# O solo con usuario (pedirá password)
git remote set-url origin https://TU_USUARIO@github.com/TU_USUARIO/recruitment-model.git
```

---

## 🛠️ TROUBLESHOOTING

### Error: "fatal: No such remote"
```bash
# Significa que el remote no existe
# Solución: crear nuevo remote
git remote add origin <URL>
```

### Error: "fatal: remote origin already exists"
```bash
# El remote ya existe
# Solución: renombrarlo primero o cambiar URL
git remote set-url origin <NUEVA_URL>
```

### Error de autenticación
```bash
# Si falla el push por autenticación

# Opción 1: Usar SSH en lugar de HTTPS
git remote set-url origin git@github.com:usuario/repo.git

# Opción 2: Guardar credenciales en Git
git config --global credential.helper store
git push  # Pedir credenciales, luego las guarda

# Opción 3: Usar token de acceso personal
git remote set-url origin https://TOKEN@github.com/usuario/repo.git
```

---

## 📊 COMPARATIVA DE MÉTODOS

| Método | Seguridad | Facilidad | Mejor Para |
|--------|-----------|-----------|-----------|
| HTTPS + Token | ⭐⭐⭐ | ⭐⭐⭐⭐ | Nuevos usuarios |
| SSH | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Usuarios avanzados |
| HTTPS + Password | ⭐⭐ | ⭐⭐⭐⭐⭐ | Tests locales |

---

## 🎯 EJEMPLO PRÁCTICO COMPLETO

### Scenario: Cambiar de GitHub a GitLab

```bash
# 1. Ver estado actual
git remote -v
# origin  https://github.com/juan/recruitment-model.git

# 2. Cambiar URL a GitLab
git remote set-url origin https://gitlab.com/juan/recruitment-model-new.git

# 3. Verificar cambio
git remote -v
# origin  https://gitlab.com/juan/recruitment-model-new.git

# 4. Hacer push
git push -u origin --all
git push -u origin --tags

# 5. Verificar en GitLab
# → Ir a https://gitlab.com/juan/recruitment-model-new
# → Debe mostrar tu código
```

---

## 📚 COMANDOS ÚTILES

```bash
# Ver todos los remotes
git remote -v

# Ver información detallada de un remote
git remote show origin

# Agregar un remote adicional
git remote add upstream https://github.com/otro/repo.git

# Renombrar remote
git remote rename origin upstream

# Eliminar remote
git remote remove origin

# Cambiar solo la URL de fetch
git remote set-url --push origin https://...

# Ver rama upstream
git branch -vv
```

---

## ⚠️ ANTES DE CAMBIAR

### Checklist

- [ ] Verificar URL actual con `git remote -v`
- [ ] Crear nuevo repositorio en el servidor destino (si es necesario)
- [ ] Tener permisos de push en el nuevo repositorio
- [ ] Backup de tu código (aunque Git lo maneja bien)
- [ ] Comunicar a tu equipo el cambio de URL

---

## ✅ DESPUÉS DE CAMBIAR

### Verificación

```bash
# 1. Ver nueva URL
git remote -v

# 2. Hacer un push pequeño
git push -u origin main

# 3. Verificar en servidor remoto
# Ir a la URL del nuevo repositorio

# 4. Confirmar que está sincronizado
git status
# On branch main
# Your branch is up to date with 'origin/main'
```

---

## 🔄 MIGRAR CON HISTORIAL COMPLETO

Si quieres mantener TODO el historial (ramas, tags, etc.):

```bash
# 1. Hacer mirror clone del repo anterior
git clone --mirror https://github.com/usuario/repo-viejo.git

# 2. Hacer mirror push al nuevo repo
cd repo-viejo.git
git push --mirror https://github.com/usuario/repo-nuevo.git

# 3. Cambiar en tu working directory
cd ../mi-proyecto
git remote set-url origin https://github.com/usuario/repo-nuevo.git
```

---

## 🎯 PARA TU PROYECTO ACTUAL

### Si quieres subir a GitHub:

```bash
cd c:\Code\Vectorizacion\recruitment_automation\modelo_entrenado_multiloss_portable

# 1. Cambiar URL
git remote set-url origin https://github.com/TU_USUARIO/recruitment-model.git

# 2. Verificar
git remote -v

# 3. Push
git push -u origin --all
git push -u origin --tags
```

### Si quieres subir a GitLab:

```bash
# 1. Cambiar URL
git remote set-url origin https://gitlab.com/TU_USUARIO/recruitment-model.git

# 2. Verificar
git remote -v

# 3. Push
git push -u origin --all
```

---

## 💡 TIPS

1. **Usa SSH para mayor seguridad** en producción
2. **Guarda credenciales localmente** con `credential.helper`
3. **Crea un .gitignore** antes de hacer push
4. **Usa tags** para versiones importantes
5. **Documenta el cambio** en tu equipo

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Pierdo mi historial al cambiar URL?**
R: No, el historial se mantiene. Solo cambias dónde se guarda.

**P: ¿Puedo tener múltiples remotes?**
R: Sí, con `git remote add` puedes agregar más.

**P: ¿Cómo cambio de rama principal (main vs master)?**
R: Los cambios de URL no afectan esto. Es independiente.

**P: ¿Necesito un token de acceso?**
R: Depende del servidor. GitHub y GitLab sí lo recomiendan.

---

**Referencia**: Git Remote Documentation  
**Versión**: 1.0  
**Última actualización**: 2026-01-19
