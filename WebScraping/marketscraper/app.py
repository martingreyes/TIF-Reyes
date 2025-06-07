from flask import Flask, request, jsonify
import subprocess
import time
import os
import json
import tempfile
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    origins=os.getenv("CORS_ALLOWED_ORIGINS", "*").split(","),
    methods=os.getenv("CORS_ALLOWED_METHODS", "GET").split(","),
    allow_headers=os.getenv("CORS_ALLOWED_HEADERS", "Content-Type,Authorization,X-Requested-With").split(","),
    expose_headers=os.getenv("CORS_EXPOSED_HEADERS", "Content-Length,Content-Range").split(","),
    supports_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
)

@app.route('/run_spider', methods=['GET'])
def run_spider():
    spider_name = request.args.get('spider_name')
    if not spider_name:
        return jsonify({'error': 'Parámetro "spider_name" requerido'}), 400

    # Crear archivo temporal para almacenar los ítems
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_output:
        output_file = temp_output.name

    start_time = time.time()

    try:
        # Ejecutar el spider y guardar resultados en JSON
        result = subprocess.run(
            ['scrapy', 'crawl', spider_name, '-o', output_file],
            capture_output=True,
            text=True,
            timeout=300 
        )

        end_time = time.time()
        time_elapsed = round(end_time - start_time, 2)

        # Leer los ítems
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                items = json.load(f)
            os.remove(output_file)
        else:
            items = []

        # Contar ítems y armar respuesta
        item_scraped_count = len(items)
        return jsonify({
            'spider_name': spider_name,
            'item_scraped_count': item_scraped_count,
            'time_elapsed_seconds': time_elapsed,
            'items': items
        })

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Scrapy spider timeout'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
