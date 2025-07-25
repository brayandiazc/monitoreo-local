# Ejemplos de Uso - Sistema de Monitoreo Local

## 🚀 Inicio Rápido

### 1. Levantar el entorno

```bash
# Levantar todos los servicios
docker-compose up -d

# Verificar que todos estén corriendo
docker-compose ps
```

### 2. Acceder a las herramientas

- **Aplicación Flask**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Kibana**: http://localhost:5601

## 📊 Ejemplos de Monitoreo

### Generar Logs desde la Aplicación Web

1. Ve a http://localhost:5000
2. Usa los botones para generar diferentes tipos de logs:
   - **Generar Log Info**: Crea logs informativos
   - **Generar Log Warning**: Crea logs de advertencia
   - **Generar Log Error**: Crea logs de error
   - **Simular Error**: Genera un error HTTP 500
   - **Proceso Largo**: Simula un proceso que toma tiempo

### Ver Logs en Kibana

1. Accede a http://localhost:5601
2. Ve a **Management** > **Stack Management**
3. En **Kibana**, selecciona **Index Patterns**
4. Crea un nuevo índice pattern: `flask-logs-*`
5. Ve a **Discover** para ver los logs en tiempo real

### Consultar Métricas en Prometheus

1. Accede a http://localhost:9090
2. Ve a la pestaña **Graph**
3. Ejecuta estas consultas:

```promql
# Total de requests HTTP
flask_http_requests_total

# Duración promedio de requests
rate(flask_http_request_duration_seconds_sum[5m]) / rate(flask_http_request_duration_seconds_count[5m])

# Total de errores
flask_errors_total

# Requests por segundo
rate(flask_http_requests_total[5m])
```

### Visualizar en Grafana

1. Accede a http://localhost:3000 (admin/admin)
2. El dashboard "Flask Application Dashboard" se carga automáticamente
3. Verás:
   - Total de requests HTTP
   - Duración de requests
   - Contador de errores

## 🔧 Ejemplos de Configuración

### Agregar una Nueva Métrica Personalizada

En `app/routes.py`, agrega:

```python
# Contador personalizado
custom_counter = metrics.counter('mi_contador_total', 'Descripción del contador')

@app.route('/mi-endpoint')
def mi_endpoint():
    custom_counter.inc()
    return jsonify({'status': 'success'})
```

### Configurar Alertas en Prometheus

Crea `prometheus/alerts.yml`:

```yaml
groups:
  - name: flask_alerts
    rules:
      - alert: FlaskHighErrorRate
        expr: rate(flask_errors_total[5m]) > 0.1
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Alta tasa de errores en Flask"
          description: "La aplicación Flask tiene una tasa de errores alta"
```

### Personalizar Logstash

En `logstash/logstash.conf`, agrega filtros:

```conf
filter {
  if [level] == "ERROR" {
    mutate {
      add_field => { "alert" => "true" }
    }
  }

  grok {
    match => { "message" => "%{GREEDYDATA:log_message}" }
  }
}
```

## 📈 Ejemplos de Consultas

### Logs en Kibana

```json
// Buscar todos los errores
{
  "query": {
    "match": {
      "level": "ERROR"
    }
  }
}

// Buscar logs de los últimos 15 minutos
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-15m"
      }
    }
  }
}

// Agrupar por nivel de log
{
  "size": 0,
  "aggs": {
    "log_levels": {
      "terms": {
        "field": "level.keyword"
      }
    }
  }
}
```

### Métricas en Prometheus

```promql
# Top 5 endpoints más usados
topk(5, sum by (endpoint) (flask_http_requests_total))

# Tasa de errores por minuto
rate(flask_errors_total[1m])

# Percentil 95 de duración de requests
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))

# Requests por segundo por método HTTP
rate(flask_http_requests_total[5m]) by (method)
```

## 🧪 Scripts de Prueba

### Generar Carga de Prueba

```bash
#!/bin/bash
# test_load.sh

echo "Generando carga de prueba..."

# Generar 100 requests
for i in {1..100}; do
  curl -s http://localhost:5000/ > /dev/null
  curl -s "http://localhost:5000/generar-log?type=info&message=Test%20$i" > /dev/null

  # Generar algunos errores
  if [ $((i % 10)) -eq 0 ]; then
    curl -s http://localhost:5000/simular-error > /dev/null
  fi

  sleep 0.1
done

echo "Carga de prueba completada"
```

### Monitorear en Tiempo Real

```bash
#!/bin/bash
# monitor.sh

echo "Monitoreando logs en tiempo real..."
echo "Presiona Ctrl+C para detener"

# Ver logs de Flask
docker-compose logs -f flask-app &

# Ver logs de Logstash
docker-compose logs -f logstash &

# Ver logs de Prometheus
docker-compose logs -f prometheus &

wait
```

## 🔍 Troubleshooting

### Verificar Estado de Servicios

```bash
# Estado general
docker-compose ps

# Logs de un servicio específico
docker-compose logs flask-app
docker-compose logs prometheus
docker-compose logs elasticsearch

# Verificar conectividad
curl http://localhost:5000/metrics
curl http://localhost:9090/api/v1/targets
curl http://localhost:9200/_cluster/health
```

### Reiniciar Servicios

```bash
# Reiniciar un servicio específico
docker-compose restart flask-app

# Reiniciar todos los servicios
docker-compose down
docker-compose up -d

# Reconstruir imagen de Flask
docker-compose build flask-app
docker-compose up -d flask-app
```

### Limpiar Datos

```bash
# Detener y limpiar volúmenes
docker-compose down -v

# Limpiar logs
rm -rf logs/*.log

# Recrear directorio de logs
mkdir -p logs
```

## 📊 Dashboards Adicionales

### Crear Dashboard Personalizado en Grafana

1. Ve a http://localhost:3000
2. Crea un nuevo dashboard
3. Agrega paneles con estas consultas:

**Panel 1: Requests por Minuto**

```promql
rate(flask_http_requests_total[1m])
```

**Panel 2: Duración Promedio**

```promql
rate(flask_http_request_duration_seconds_sum[5m]) / rate(flask_http_request_duration_seconds_count[5m])
```

**Panel 3: Tasa de Errores**

```promql
rate(flask_errors_total[5m])
```

### Visualización en Kibana

1. Ve a **Visualize**
2. Crea un gráfico de líneas con:
   - Índice: `flask-logs-*`
   - Métrica: Count
   - Buckets: Date Histogram en `@timestamp`
   - Split Series: Terms en `level.keyword`

## 🎯 Casos de Uso Comunes

### Monitoreo de Producción

- Configurar alertas en Prometheus
- Crear dashboards específicos en Grafana
- Configurar retención de logs en Elasticsearch
- Implementar backup de volúmenes Docker

### Desarrollo Local

- Usar para probar nuevas métricas
- Validar configuración de logging
- Probar alertas antes de producción
- Desarrollar dashboards personalizados

### Debugging

- Usar Kibana para buscar logs específicos
- Analizar patrones de errores
- Monitorear rendimiento de endpoints
- Identificar cuellos de botella
