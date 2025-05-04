from flask import Flask, jsonify, request # type: ignore
from main.MariaDBClient import MariaDBClient
from dotenv import load_dotenv
import logging

app = Flask(__name__)

load_dotenv()

mariadbclient = MariaDBClient()

@app.route('/info')
def get_info():
    data = mariadbclient.get_info()
    return jsonify(data), 200

@app.route('/productos/')
def get_productos():
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
