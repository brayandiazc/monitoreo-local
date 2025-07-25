#!/bin/bash

# Script de inicio rápido para el Sistema de Monitoreo Local
# Autor: Sistema de Monitoreo Local
# Versión: 1.0.0

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si Docker está corriendo
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker no está corriendo. Por favor, inicia Docker y vuelve a intentar."
        exit 1
    fi
    print_success "Docker está corriendo"
}

# Función para verificar puertos disponibles
check_ports() {
    local ports=("5000" "9090" "3000" "5601" "9200" "5044" "8080")
    local occupied_ports=()
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            occupied_ports+=($port)
        fi
    done
    
    if [ ${#occupied_ports[@]} -gt 0 ]; then
        print_warning "Los siguientes puertos están ocupados: ${occupied_ports[*]}"
        print_warning "Esto puede causar conflictos al levantar los servicios"
        read -p "¿Deseas continuar de todas formas? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Operación cancelada"
            exit 1
        fi
    else
        print_success "Todos los puertos están disponibles"
    fi
}

# Función para levantar servicios
start_services() {
    print_status "Levantando servicios con Docker Compose..."
    
    if docker-compose up -d; then
        print_success "Servicios levantados correctamente"
    else
        print_error "Error al levantar los servicios"
        exit 1
    fi
}

# Función para esperar a que los servicios estén listos
wait_for_services() {
    print_status "Esperando a que los servicios estén listos..."
    
    local services=("flask-app" "prometheus" "elasticsearch" "grafana" "kibana")
    local max_attempts=30
    local attempt=1
    
    for service in "${services[@]}"; do
        print_status "Verificando $service..."
        
        while [ $attempt -le $max_attempts ]; do
            if docker-compose ps $service | grep -q "Up"; then
                print_success "$service está listo"
                break
            fi
            
            if [ $attempt -eq $max_attempts ]; then
                print_warning "$service no está listo después de $max_attempts intentos"
            fi
            
            sleep 2
            ((attempt++))
        done
        attempt=1
    done
}

# Función para mostrar información de acceso
show_access_info() {
    echo
    echo "=========================================="
    echo "🚀 SISTEMA DE MONITOREO LOCAL"
    echo "=========================================="
    echo
    echo "📊 HERRAMIENTAS DISPONIBLES:"
    echo "------------------------------------------"
    echo "🌐 Aplicación Flask:    http://localhost:5000"
    echo "📈 Prometheus:          http://localhost:9090"
    echo "📊 Grafana:             http://localhost:3000 (admin/admin)"
    echo "🔍 Kibana:              http://localhost:5601"
    echo "🔧 Elasticsearch:       http://localhost:9200"
    echo "📝 Logstash:            Puerto 5044"
    echo "📊 Graphite:            http://localhost:8080"
    echo
    echo "📋 COMANDOS ÚTILES:"
    echo "------------------------------------------"
    echo "Ver estado:             docker-compose ps"
    echo "Ver logs:               docker-compose logs -f"
    echo "Detener servicios:      docker-compose down"
    echo "Reiniciar:              docker-compose restart"
    echo
    echo "🧪 PRUEBAS RÁPIDAS:"
    echo "------------------------------------------"
    echo "1. Ve a http://localhost:5000"
    echo "2. Usa los botones para generar logs"
    echo "3. Verifica métricas en Prometheus"
    echo "4. Explora logs en Kibana"
    echo "5. Ve dashboards en Grafana"
    echo
    echo "📚 DOCUMENTACIÓN:"
    echo "------------------------------------------"
    echo "README.md:              Instrucciones completas"
    echo "EJEMPLO_USO.md:         Ejemplos de uso"
    echo
    echo "=========================================="
}

# Función para verificar estado de servicios
check_services_status() {
    print_status "Verificando estado de servicios..."
    echo
    docker-compose ps
    echo
}

# Función principal
main() {
    echo "🚀 Iniciando Sistema de Monitoreo Local..."
    echo "=========================================="
    echo
    
    # Verificar Docker
    check_docker
    
    # Verificar puertos
    check_ports
    
    # Levantar servicios
    start_services
    
    # Esperar a que estén listos
    wait_for_services
    
    # Mostrar estado
    check_services_status
    
    # Mostrar información de acceso
    show_access_info
    
    print_success "¡Sistema de monitoreo iniciado correctamente!"
    print_status "Puedes acceder a las herramientas usando los enlaces de arriba"
}

# Manejo de argumentos
case "${1:-}" in
    "status")
        check_services_status
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "stop")
        print_status "Deteniendo servicios..."
        docker-compose down
        print_success "Servicios detenidos"
        ;;
    "restart")
        print_status "Reiniciando servicios..."
        docker-compose down
        docker-compose up -d
        print_success "Servicios reiniciados"
        ;;
    "clean")
        print_warning "Esto eliminará todos los datos. ¿Estás seguro? (y/N): "
        read -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Limpiando datos..."
            docker-compose down -v
            rm -rf logs/*.log 2>/dev/null || true
            print_success "Datos limpiados"
        else
            print_status "Operación cancelada"
        fi
        ;;
    "help"|"-h"|"--help")
        echo "Uso: $0 [comando]"
        echo
        echo "Comandos:"
        echo "  (sin comando)  Iniciar todos los servicios"
        echo "  status         Mostrar estado de servicios"
        echo "  logs           Mostrar logs en tiempo real"
        echo "  stop           Detener todos los servicios"
        echo "  restart        Reiniciar todos los servicios"
        echo "  clean          Limpiar todos los datos"
        echo "  help           Mostrar esta ayuda"
        ;;
    "")
        main
        ;;
    *)
        print_error "Comando desconocido: $1"
        echo "Usa '$0 help' para ver comandos disponibles"
        exit 1
        ;;
esac 