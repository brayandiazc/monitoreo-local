import time
import random
from flask import render_template, request, jsonify
from app import create_app
from prometheus_flask_exporter import PrometheusMetrics

app = create_app()
metrics = PrometheusMetrics(app, path='/metrics')

# Contador personalizado para errores
error_counter = metrics.counter('flask_errors_total', 'Total de errores simulados')

@app.route('/')
def index():
    app.logger.info('Acceso a la página de inicio')
    return render_template('index.html')

@app.route('/acerca-de')
def about():
    app.logger.info('Acceso a la página acerca de')
    return render_template('about.html')

@app.route('/contacto')
def contact():
    app.logger.info('Acceso a la página de contacto')
    return render_template('contact.html')

@app.route('/simular-error')
def simulate_error():
    app.logger.error('Error simulado generado')
    error_counter.inc()
    return jsonify({
        'error': 'Error simulado generado',
        'timestamp': time.time()
    }), 500

@app.route('/proceso-largo')
def long_process():
    app.logger.info('Iniciando proceso largo')
    
    # Simular proceso que toma tiempo
    time.sleep(random.uniform(2, 5))
    
    app.logger.info('Proceso largo completado')
    return jsonify({
        'message': 'Proceso largo completado',
        'duration': random.uniform(2, 5),
        'timestamp': time.time()
    })

@app.route('/generar-log')
def generate_log():
    log_type = request.args.get('type', 'info')
    message = request.args.get('message', 'Log generado')
    
    if log_type == 'error':
        app.logger.error(message)
    elif log_type == 'warning':
        app.logger.warning(message)
    else:
        app.logger.info(message)
    
    return jsonify({
        'status': 'success',
        'log_type': log_type,
        'message': message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 