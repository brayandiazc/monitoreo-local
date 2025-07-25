#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración del entorno de monitoreo
"""

import os
import sys
import json
from pathlib import Path

def check_files():
    """Verificar que todos los archivos necesarios existan"""
    required_files = [
        'docker-compose.yml',
        'Dockerfile',
        'requirements.txt',
        'run.py',
        'app/__init__.py',
        'app/routes.py',
        'app/templates/base.html',
        'app/templates/index.html',
        'app/templates/about.html',
        'app/templates/contact.html',
        'prometheus/prometheus.yml',
        'logstash/logstash.conf',
        'grafana/provisioning/datasources/prometheus.yml',
        'grafana/provisioning/dashboards/dashboard.yml',
        'grafana/provisioning/dashboards/flask-dashboard.json',
        'fluentd/fluent.conf',
        'README.md',
        '.gitignore'
    ]
    
    print("🔍 Verificando archivos...")
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Faltan {len(missing_files)} archivos:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print(f"\n✅ Todos los {len(required_files)} archivos están presentes")
        return True

def check_docker_compose():
    """Verificar que docker-compose.yml sea válido"""
    print("\n🐳 Verificando docker-compose.yml...")
    
    try:
        import yaml
        with open('docker-compose.yml', 'r') as f:
            yaml.safe_load(f)
        print("  ✅ docker-compose.yml es válido")
        return True
    except ImportError:
        print("  ⚠️  PyYAML no está instalado, no se puede verificar la sintaxis")
        return True
    except Exception as e:
        print(f"  ❌ Error en docker-compose.yml: {e}")
        return False

def check_requirements():
    """Verificar requirements.txt"""
    print("\n📦 Verificando requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        if len(requirements) >= 3:
            print(f"  ✅ {len(requirements)} dependencias encontradas")
            for req in requirements:
                print(f"    - {req}")
            return True
        else:
            print("  ❌ Muy pocas dependencias en requirements.txt")
            return False
    except Exception as e:
        print(f"  ❌ Error leyendo requirements.txt: {e}")
        return False

def check_prometheus_config():
    """Verificar configuración de Prometheus"""
    print("\n📊 Verificando configuración de Prometheus...")
    
    try:
        with open('prometheus/prometheus.yml', 'r') as f:
            config = f.read()
        
        if 'flask-app:5000' in config and '/metrics' in config:
            print("  ✅ Configuración de Prometheus correcta")
            return True
        else:
            print("  ❌ Configuración de Prometheus incompleta")
            return False
    except Exception as e:
        print(f"  ❌ Error leyendo prometheus.yml: {e}")
        return False

def check_logstash_config():
    """Verificar configuración de Logstash"""
    print("\n📝 Verificando configuración de Logstash...")
    
    try:
        with open('logstash/logstash.conf', 'r') as f:
            config = f.read()
        
        if 'elasticsearch:9200' in config and '/logs/app.log' in config:
            print("  ✅ Configuración de Logstash correcta")
            return True
        else:
            print("  ❌ Configuración de Logstash incompleta")
            return False
    except Exception as e:
        print(f"  ❌ Error leyendo logstash.conf: {e}")
        return False

def check_ports():
    """Verificar que los puertos no estén en uso"""
    print("\n🔌 Verificando puertos...")
    
    ports = [5000, 9090, 3000, 5601, 9200, 5044, 8080]
    import socket
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"  ⚠️  Puerto {port} está en uso")
        else:
            print(f"  ✅ Puerto {port} está libre")
    
    return True

def main():
    """Función principal"""
    print("🚀 Verificación del Entorno de Monitoreo Local")
    print("=" * 50)
    
    checks = [
        check_files,
        check_docker_compose,
        check_requirements,
        check_prometheus_config,
        check_logstash_config,
        check_ports
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ Todas las verificaciones pasaron ({passed}/{total})")
        print("\n🎉 El entorno está listo para usar!")
        print("\nPara iniciar los servicios:")
        print("  docker-compose up -d")
        print("\nPara verificar el estado:")
        print("  docker-compose ps")
    else:
        print(f"❌ {total - passed} verificaciones fallaron ({passed}/{total})")
        print("\n🔧 Por favor, corrige los errores antes de continuar")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 