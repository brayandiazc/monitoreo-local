# GitHub Actions - Sistema de Monitoreo Local

Este documento describe los workflows de GitHub Actions implementados para automatizar el CI/CD del proyecto.

## 📋 Workflows Disponibles

### 1. CI/CD Pipeline Principal (`ci.yml`)

**Trigger:** Push a `main`/`develop` y Pull Requests

**Jobs:**

- **Test**: Pruebas de la aplicación Flask
- **Security**: Escaneo de vulnerabilidades
- **Docker Build**: Construcción y push de imagen Docker
- **Integration Test**: Pruebas de integración
- **Release**: Creación automática de releases

**Características:**

- ✅ Linting con flake8
- ✅ Formato con black
- ✅ Pruebas de la aplicación
- ✅ Construcción de imagen Docker
- ✅ Escaneo de seguridad con Trivy
- ✅ Tests de integración
- ✅ Releases automáticos

### 2. Docker Compose Integration Test (`docker-compose-test.yml`)

**Trigger:** Push a `main`/`develop`, Pull Requests, Manual

**Jobs:**

- **Test Complete Stack**: Prueba todo el stack de monitoreo

**Características:**

- ✅ Levanta todos los servicios con docker-compose
- ✅ Prueba endpoints de Flask
- ✅ Verifica Prometheus
- ✅ Verifica Elasticsearch
- ✅ Verifica Kibana
- ✅ Verifica Grafana
- ✅ Genera datos de prueba
- ✅ Verifica procesamiento de logs y métricas

### 3. Security Analysis (`security.yml`)

**Trigger:** Push a `main`/`develop`, Pull Requests, Semanal

**Jobs:**

- **Security Scan**: Escaneo de código fuente
- **Docker Security**: Escaneo de imagen Docker
- **Dependency Check**: Verificación de dependencias

**Herramientas:**

- 🔍 Trivy (vulnerabilidades)
- 🔍 Bandit (análisis de código Python)
- 🔍 Safety (vulnerabilidades en dependencias)
- 🔍 Hadolint (linting de Dockerfile)
- 🔍 pip-audit (auditoría de dependencias)

### 4. Deploy (`deploy.yml`)

**Trigger:** Tags, Manual

**Jobs:**

- **Deploy to Staging**: Despliegue a staging
- **Deploy to Production**: Despliegue a producción
- **Notify**: Notificaciones de estado

**Características:**

- 🚀 Despliegue automático con tags
- 🚀 Despliegue manual a staging/producción
- 🚀 Health checks post-despliegue
- 🚀 Notificaciones de estado

### 5. Update Dependencies (`update-dependencies.yml`)

**Trigger:** Semanal, Manual

**Jobs:**

- **Update Dependencies**: Actualización automática de dependencias

**Características:**

- 🔄 Actualización semanal automática
- 🔄 Creación de Pull Requests
- 🔄 Revisión automática de cambios

### 6. CodeQL Analysis (`codeql.yml`)

**Trigger:** Push a `main`/`develop`, Pull Requests, Semanal

**Jobs:**

- **Analyze**: Análisis de seguridad del código

**Características:**

- 🔒 Análisis de seguridad semántico
- 🔒 Detección de vulnerabilidades
- 🔒 Análisis de flujo de datos

## 🛠️ Configuración

### Secrets Requeridos

```bash
# Para despliegue (opcional)
DEPLOY_SSH_KEY          # Clave SSH para servidor de despliegue
DEPLOY_HOST             # Host del servidor
DEPLOY_USER             # Usuario del servidor

# Para notificaciones (opcional)
SLACK_WEBHOOK_URL       # Webhook de Slack
DISCORD_WEBHOOK_URL     # Webhook de Discord
```

### Environments

Configura estos environments en GitHub:

1. **staging**: Para despliegues de staging
2. **production**: Para despliegues de producción

### Permissions

Los workflows requieren estos permisos:

```yaml
permissions:
  contents: read
  packages: write
  security-events: write
  actions: read
```

## 📊 Badges

Agrega estos badges a tu README:

```markdown
![CI/CD](https://github.com/{username}/{repo}/workflows/CI%2FCD%20Pipeline/badge.svg)
![Security](https://github.com/{username}/{repo}/workflows/Security%20Analysis/badge.svg)
![Docker](https://github.com/{username}/{repo}/workflows/Docker%20Compose%20Integration%20Test/badge.svg)
![CodeQL](https://github.com/{username}/{repo}/workflows/CodeQL/badge.svg)
```

## 🔧 Uso

### Despliegue Manual

1. Ve a **Actions** en GitHub
2. Selecciona **Deploy**
3. Haz clic en **Run workflow**
4. Selecciona el ambiente (staging/producción)
5. Ejecuta

### Actualización de Dependencias

1. Ve a **Actions** en GitHub
2. Selecciona **Update Dependencies**
3. Haz clic en **Run workflow**
4. Revisa el Pull Request generado

### Verificación de Seguridad

Los análisis de seguridad se ejecutan automáticamente, pero puedes:

1. Ve a **Security** en GitHub
2. Revisa **Code scanning alerts**
3. Revisa **Dependabot alerts**

## 📈 Monitoreo de Workflows

### Métricas Disponibles

- **Tiempo de ejecución**: Duración de cada workflow
- **Tasa de éxito**: Porcentaje de workflows exitosos
- **Tiempo de respuesta**: Desde push hasta deploy
- **Vulnerabilidades**: Número de alertas de seguridad

### Alertas

Configura alertas para:

- Workflows fallidos
- Nuevas vulnerabilidades
- Despliegues fallidos
- Dependencias desactualizadas

## 🔍 Troubleshooting

### Problemas Comunes

**Workflow falla en tests:**

```bash
# Ejecuta localmente
python test_setup.py
docker-compose up -d
```

**Docker build falla:**

```bash
# Verifica Dockerfile
docker build -t test .
```

**Security scan falla:**

```bash
# Instala herramientas localmente
pip install bandit safety
bandit -r app/
safety check
```

**Deploy falla:**

- Verifica secrets configurados
- Verifica permisos del repositorio
- Verifica conectividad del servidor

### Logs y Debugging

1. Ve a **Actions** en GitHub
2. Selecciona el workflow fallido
3. Revisa los logs del job específico
4. Descarga artifacts si están disponibles

## 🚀 Optimizaciones

### Cache

Los workflows usan cache para:

- Dependencias de pip
- Imágenes de Docker
- Build de CodeQL

### Paralelización

Los jobs se ejecutan en paralelo cuando es posible:

- Test y Security pueden ejecutarse simultáneamente
- Docker build espera a que Test y Security terminen
- Integration test puede ejecutarse en paralelo con Docker build

### Timeouts

Configurados para evitar ejecuciones infinitas:

- Jobs individuales: 30 minutos
- Workflows completos: 2 horas
- Despliegues: 15 minutos

## 📝 Personalización

### Agregar Nuevos Tests

1. Crea un nuevo job en `ci.yml`
2. Agrega los steps necesarios
3. Configura dependencias con `needs:`

### Agregar Nuevas Herramientas de Seguridad

1. Agrega el step en `security.yml`
2. Configura el output
3. Agrega notificaciones si es necesario

### Modificar Despliegue

1. Edita `deploy.yml`
2. Agrega steps específicos para tu infraestructura
3. Configura secrets adicionales

## 🔄 Mantenimiento

### Actualización de Actions

Dependabot actualiza automáticamente las GitHub Actions.

### Limpieza

Los artifacts se limpian automáticamente:

- Logs: 7 días
- Security results: 30 días
- Build cache: 7 días

### Monitoreo

Revisa regularmente:

- Tiempo de ejecución de workflows
- Tasa de éxito
- Alertas de seguridad
- Uso de recursos

## 📚 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CodeQL Documentation](https://docs.github.com/en/code-security/code-scanning)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Security Best Practices](https://docs.github.com/en/code-security/security-overview)
