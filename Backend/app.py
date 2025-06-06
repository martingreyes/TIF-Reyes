from flask import Flask, jsonify, request # type: ignore
from main.MariaDBClient import MariaDBClient
from main.ResourceLockManager import ResourceLockManager
from dotenv import load_dotenv
import logging
from flask_cors import CORS # type: ignore
import os

app = Flask(__name__)

CORS(
    app,
    origins=os.getenv("CORS_ALLOWED_ORIGINS", "*").split(","),
    methods=os.getenv("CORS_ALLOWED_METHODS", "GET").split(","),
    allow_headers=os.getenv("CORS_ALLOWED_HEADERS", "Content-Type,Authorization,X-Requested-With").split(","),
    expose_headers=os.getenv("CORS_EXPOSED_HEADERS", "Content-Length,Content-Range").split(","),
    supports_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
)

load_dotenv()

mariadbclient = MariaDBClient()
lock_manager = ResourceLockManager()

@app.route('/api/info')
def get_info():
    if lock_manager.is_locked():
        return jsonify({"error": "La base de datos está siendo actualizada. Intenta nuevamente en unos minutos."}), 423
    data = mariadbclient.get_info()
    return jsonify(data), 200

@app.route('/api/productos')
def get_productos():
    if lock_manager.is_locked():
        return jsonify({"error": "La base de datos está siendo actualizada. Intenta nuevamente en unos minutos."}), 423
    categoria = request.args.get('categoria')
    descripcion = request.args.get('descripcion')

    if categoria:
        data = mariadbclient.get_products_by_category(categoria)
        cantidad_total_productos = sum(len(subgrupo) for subgrupo in data)
        response = {
            "categoria": categoria,
            "cantidad_productos": cantidad_total_productos,
            "data": data
        }

    elif descripcion:
        data = mariadbclient.get_products_by_description(descripcion)
        cantidad_total_productos = sum(len(subgrupo) for subgrupo in data)
        response = {
            "descripcion": descripcion,
            "cantidad_productos": cantidad_total_productos,
            "data": data
        }

    else:
        return jsonify({"error": "Debe proporcionar al menos un parámetro: 'categoria' o 'descripcion'"}), 400

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
