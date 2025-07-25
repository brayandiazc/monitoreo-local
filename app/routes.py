import time
import random
from flask import render_template, request, jsonify, current_app, Blueprint
from prometheus_flask_exporter import PrometheusMetrics

# Crear blueprint
main = Blueprint('main', __name__)

# Variable global para las métricas
metrics = None
error_counter = None

def init_metrics(app):
    global metrics, error_counter
    metrics = PrometheusMetrics(app, path='/metrics')
    error_counter = metrics.counter('flask_errors_total', 'Total de errores simulados')

@main.route('/')
def index():
    current_app.logger.info('Acceso a la página de inicio')
    return render_template('index.html')

@main.route('/acerca-de')
def about():
    current_app.logger.info('Acceso a la página acerca de')
    return render_template('about.html')

@main.route('/contacto')
def contact():
    current_app.logger.info('Acceso a la página de contacto')
    return render_template('contact.html')

@main.route('/simular-error')
def simulate_error():
    current_app.logger.error('Error simulado generado')
    if error_counter:
        error_counter.inc()
    return jsonify({
        'error': 'Error simulado generado',
        'timestamp': time.time()
    }), 500

@main.route('/proceso-largo')
def long_process():
    current_app.logger.info('Iniciando proceso largo')
    
    # Simular proceso que toma tiempo
    time.sleep(random.uniform(2, 5))
    
    current_app.logger.info('Proceso largo completado')
    return jsonify({
        'message': 'Proceso largo completado',
        'duration': random.uniform(2, 5),
        'timestamp': time.time()
    })

@main.route('/generar-log')
def generate_log():
    log_type = request.args.get('type', 'info')
    message = request.args.get('message', 'Log generado')
    
    if log_type == 'error':
        current_app.logger.error(message)
    elif log_type == 'warning':
        current_app.logger.warning(message)
    else:
        current_app.logger.info(message)
    
    return jsonify({
        'status': 'success',
        'log_type': log_type,
        'message': message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 