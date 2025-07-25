import os
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

def create_app():
    app = Flask(__name__)
    
    # Configurar logging
    if not app.debug:
        # Logging a archivo
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Handler para archivo con rotación
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        
        # Formato JSON para logs
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Configurar logger de la aplicación
        app.logger.addHandler(file_handler)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.INFO)
        
        app.logger.info('Aplicación Flask iniciada')
    
    # Configurar métricas de Prometheus
    metrics = PrometheusMetrics(app, path='/metrics')
    
    # Importar rutas
    from app import routes
    
    return app 