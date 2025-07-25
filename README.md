# Sistema de Monitoreo Local

Un entorno completo de monitoreo local usando Docker Compose que incluye Flask, Prometheus, Grafana y ELK Stack.

## 🚀 Características

- **Aplicación Flask** con logging estructurado y métricas automáticas
- **Prometheus** para recolección y almacenamiento de métricas
- **Grafana** para visualización de dashboards
- **ELK Stack** (Elasticsearch, Logstash, Kibana) para análisis de logs
- **Fluentd + Graphite** (opcional) para demostrar el stack GFG
- **Docker Compose** para orquestación completa

## 📋 Prerrequisitos

- Docker
- Docker Compose
- Al menos 4GB de RAM disponible

## 🛠️ Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd monitoreo-local
```

### 2. Levantar todos los servicios

```bash
docker-compose up -d
```

### 3. Verificar que todos los servicios estén corriendo

```bash
docker-compose ps
```

## 🌐 Acceso a las Herramientas

| Servicio             | URL                   | Credenciales |
| -------------------- | --------------------- | ------------ |
| **Aplicación Flask** | http://localhost:5000 | -            |
| **Prometheus**       | http://localhost:9090 | -            |
| **Grafana**          | http://localhost:3000 | admin/admin  |
| **Kibana**           | http://localhost:5601 | -            |
| **Elasticsearch**    | http://localhost:9200 | -            |
| **Graphite**         | http://localhost:8080 | -            |

## 📊 Funcionalidades de la Aplicación Flask

### Páginas Web

- **Inicio** (`/`): Panel de control con botones de prueba
- **Acerca de** (`/acerca-de`): Información del proyecto
- **Contacto** (`/contacto`): Información de contacto y soporte

### Endpoints de Prueba

- **Generar Log** (`/generar-log?type=info&message=texto`): Genera logs de diferentes niveles
- **Simular Error** (`/simular-error`): Genera un error HTTP 500
- **Proceso Largo** (`/proceso-largo`): Simula un proceso que toma tiempo
- **Métricas** (`/metrics`): Endpoint de Prometheus con métricas de Flask

## 🔧 Configuración

### Prometheus

- Configuración: `prometheus/prometheus.yml`
- Scrapea la aplicación Flask cada 10 segundos
- Almacena datos por 200 horas

### Logstash

- Configuración: `logstash/logstash.conf`
- Lee logs JSON de Flask desde `/logs/app.log`
- Envía logs a Elasticsearch con índices por fecha

### Grafana

- Datasource Prometheus configurado automáticamente
- Dashboard básico de Flask incluido
- Credenciales: admin/admin

### ELK Stack

- Elasticsearch: Motor de búsqueda
- Logstash: Procesamiento de logs
- Kibana: Visualización de logs

## 📈 Dashboards y Visualizaciones

### Grafana

- **Flask Application Dashboard**: Métricas básicas de la aplicación
  - Total de requests HTTP
  - Duración de requests
  - Contador de errores

### Kibana

- **Logs de Flask**: Visualización de logs en tiempo real
- **Análisis por nivel**: Filtros por INFO, WARNING, ERROR
- **Búsqueda avanzada**: Consultas Elasticsearch

## 🧪 Pruebas

### 1. Generar Logs

Usa los botones en la página de inicio para generar diferentes tipos de logs:

- Logs informativos
- Logs de advertencia
- Logs de error

### 2. Simular Errores

Haz clic en "Simular Error" para generar errores HTTP 500 y ver cómo se incrementa el contador en Prometheus.

### 3. Procesos Largos

Ejecuta "Proceso Largo" para simular operaciones que toman tiempo y ver las métricas de duración.

### 4. Verificar Métricas

- Accede a http://localhost:5000/metrics para ver las métricas raw
- Ve a Prometheus para consultar métricas específicas
- Usa Grafana para visualizaciones

## 🔍 Monitoreo de Logs

### En Kibana

1. Ve a http://localhost:5601
2. Crea un índice pattern: `flask-logs-*`
3. Explora los logs en Discover
4. Crea visualizaciones en Visualize

### Logs Disponibles

- **INFO**: Accesos a páginas, procesos iniciados
- **WARNING**: Advertencias del sistema
- **ERROR**: Errores simulados y del sistema

## 🐛 Solución de Problemas

### Servicios no inician

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs flask-app

# Reiniciar todos los servicios
docker-compose down
docker-compose up -d
```

### Puertos ocupados

Verifica que los siguientes puertos estén libres:

- 5000 (Flask)
- 9090 (Prometheus)
- 3000 (Grafana)
- 5601 (Kibana)
- 9200 (Elasticsearch)

### Logs no aparecen en Kibana

1. Verifica que Elasticsearch esté corriendo: `curl http://localhost:9200`
2. Verifica que Logstash esté procesando: `docker-compose logs logstash`
3. Espera unos minutos para que los logs se indexen

### Métricas no aparecen en Prometheus

1. Verifica que Flask esté corriendo: `curl http://localhost:5000/metrics`
2. Verifica la configuración de Prometheus
3. Revisa los targets en http://localhost:9090/targets

## 📁 Estructura del Proyecto

```
monitoreo-local/
├── app/                    # Aplicación Flask
│   ├── __init__.py        # Configuración de la app
│   ├── routes.py          # Rutas y endpoints
│   └── templates/         # Plantillas HTML
├── logs/                  # Directorio de logs (volumen compartido)
├── prometheus/            # Configuración de Prometheus
│   └── prometheus.yml
├── logstash/              # Configuración de Logstash
│   └── logstash.conf
├── grafana/               # Configuración de Grafana
│   └── provisioning/
├── fluentd/               # Configuración de Fluentd
│   └── fluent.conf
├── docker-compose.yml     # Orquestación de servicios
├── Dockerfile            # Imagen de Flask
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

## 🚀 Comandos Útiles

```bash
# Levantar servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir imagen de Flask
docker-compose build flask-app

# Ver estado de servicios
docker-compose ps

# Limpiar volúmenes (cuidado: borra datos)
docker-compose down -v
```

## 📝 Notas

- Todos los datos se almacenan en volúmenes Docker locales
- No se requiere configuración adicional
- Los servicios se reinician automáticamente
- El entorno está optimizado para desarrollo local

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 🚀 GitHub Actions

Este proyecto incluye workflows de GitHub Actions para automatización completa del CI/CD:

### Workflows Disponibles

- **CI/CD Pipeline**: Pruebas, seguridad, construcción y despliegue
- **Docker Compose Test**: Pruebas de integración del stack completo
- **Security Analysis**: Escaneo de vulnerabilidades y análisis de seguridad
- **Deploy**: Despliegue automático a staging y producción
- **Update Dependencies**: Actualización automática de dependencias
- **CodeQL**: Análisis de seguridad del código

### Badges

[![CI/CD](https://github.com/{username}/{repo}/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/{username}/{repo}/actions)
[![Security](https://github.com/{username}/{repo}/workflows/Security%20Analysis/badge.svg)](https://github.com/{username}/{repo}/actions)
[![Docker](https://github.com/{username}/{repo}/workflows/Docker%2FCompose%20Integration%20Test/badge.svg)](https://github.com/{username}/{repo}/actions)
[![CodeQL](https://github.com/{username}/{repo}/workflows/CodeQL/badge.svg)](https://github.com/{username}/{repo}/actions)

### Documentación

Para más detalles sobre los GitHub Actions, consulta [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md).

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
