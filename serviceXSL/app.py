# PROJECTSOA/app.py

from flask import Flask, request, jsonify
import os
import sys

# Añade el directorio raíz del proyecto al path de Python
# para poder importar 'services' correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar la clase de tu servicio XLS
from services.serviceXSL import XLStoJSONConverter

# --- Inicialización de Flask ---
app = Flask(__name__)

# --- Configuración para microesb (simplificado por ahora) ---
# Aquí es donde necesitarás referenciar la documentación de microesb
# para saber cómo inicializarlo y registrar tus servicios.
# Basado en la documentación, microesb usa un sistema de configuración
# para mapear servicios.

# Ejemplo simplificado de cómo podrías instanciar tu convertidor de XLS
# y, conceptualmente, "registrarlo" en un ESB que te permita llamarlo.
# El microesb tiene una forma más formal de hacerlo que deberás implementar.

# xls_converter_instance = XLStoJSONConverter(data_dir=os.path.join(os.path.dirname(__file__), '..', 'data'))
xls_converter_instance = XLStoJSONConverter(data_dir='data')
# --- Configuración de la Base de Datos (usando psycopg2 y os.environ) ---
# Esto es conceptual, una aplicación real usaría un ORM como SQLAlchemy
import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# --- Rutas de Flask ---

@app.route('/')
def hello_world():
    return '¡Hola desde el servicio ServiceXSL Flask!'

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cur = conn.cursor()
    products = []
    try:
        cur.execute("SELECT id, nombre, descripcion, categoria, precio FROM productos;")
        rows = cur.fetchall()
        for row in rows:
            products.append({
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "categoria": row[3],
                "precio": float(row[4])
            })
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
    return jsonify(products)

@app.route('/catalog', methods=['GET'])
def get_catalog_as_json():
    try:
        # Nombre del archivo dentro de /app/data
        filename = 'catalog.xls'
        
        # Procesar archivo usando la instancia del convertidor
        json_output = xls_converter_instance.process_xls_file(filename)
        
        return json_output, 200, {'Content-Type': 'application/json'}
    
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error al procesar catalog.xls: {e}"}), 500

@app.route('/convert-xls-to-json', methods=['POST'])
def convert_xls():
    # En un escenario real, aquí podrías recibir el archivo XLS
    # directamente en el request, o el nombre de un archivo ya subido.
    # Por simplicidad, asumimos que se pasa el nombre del archivo de 'data/'
    
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({"error": "Se requiere 'filename' en el cuerpo JSON"}), 400

    filename = data['filename']
    
    # Llama a tu servicio de conversión de XLS
    # La integración real con microesb será más compleja, esto es un placeholder
    try:
        json_output = xls_converter_instance.process_xls_file(filename)
        if json_output:
            return json_output, 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"error": "Error al procesar el archivo XLS"}), 500
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {e}"}), 500

# Para ejecutar Flask directamente (principalmente para desarrollo local sin Docker)
if __name__ == '__main__':
    # No usar esto en producción con Gunicorn/Waitress/etc.
    app.run(host='0.0.0.0', port=5400, debug=True)