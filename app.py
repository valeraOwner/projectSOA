# app.py
from flask import Flask, request, jsonify, send_from_directory # Importamos send_from_directory
from flask_cors import CORS # <--- ¡IMPORTA CORS!
import os
import sys

# Añadir el directorio raíz del proyecto al sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar las configuraciones del ESB (mantén esto como lo tenías antes de la depuración de Flasgger)
from microesb import microesb
from microesb_config.service_properties import ALL_SERVICE_PROPERTIES, service_properties_product, service_properties_messaging, service_properties_xls
from microesb_config.class_reference import ALL_CLASS_REFERENCES, class_reference_product, class_reference_messaging, class_reference_xls
from microesb_config.class_mapping import ALL_CLASS_MAPPINGS, class_mapping_product, class_mapping_messaging, class_mapping_xls


app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN PARA SERVIR SWAGGER UI MANUALMENTE ---
# En este enfoque, no usamos Flasgger para parsear el YAML, solo para servir el UI.
# Necesitas instalar Flask-Swagger-UI: pip install flask-swagger-ui
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/apidocs"  # URL para el Swagger UI
API_URL = "/static/openapi.yaml"  # URL donde Flask servirá tu archivo openapi.yaml

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API del ESB de Catálogo"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Ruta para servir el archivo openapi.yaml directamente
@app.route('/static/<path:filename>')
def static_content(filename):
    return send_from_directory(project_root, filename) # Sirve desde la raíz del proyecto

# --- MAPEO DE SYSServiceID LÓGICO A CLASS HANDLER Y SUS CONFIGURACIONES ---
SERVICE_ID_TO_CONFIG_MAP = {
    'getProductById': {'handler': 'Product', 'ref': class_reference_product, 'map': class_mapping_product, 'props': service_properties_product},
    'createProduct': {'handler': 'Product', 'ref': class_reference_product, 'map': class_mapping_product, 'props': service_properties_product},
    'updateProductById': {'handler': 'Product', 'ref': class_reference_product, 'map': class_mapping_product, 'props': service_properties_product},
    'deleteProductById': {'handler': 'Product', 'ref': class_reference_product, 'map': class_mapping_product, 'props': service_properties_product},
    'sendPurchaseNotification': {'handler': 'MessagingService', 'ref': class_reference_messaging, 'map': class_mapping_messaging, 'props': service_properties_messaging},
    'registerLogEvent': {'handler': 'MessagingService', 'ref': class_reference_messaging, 'map': class_mapping_messaging, 'props': service_properties_messaging},
    'getById': {'handler': 'ExcelCatalogoHandler', 'ref': class_reference_xls, 'map': class_mapping_xls, 'props': service_properties_xls},
    'listAll': {'handler': 'ExcelCatalogoHandler', 'ref': class_reference_xls, 'map': class_mapping_xls, 'props': service_properties_xls},
    'searchByName': {'handler': 'ExcelCatalogoHandler', 'ref': class_reference_xls, 'map': class_mapping_xls, 'props': service_properties_xls}
}

# Endpoint principal para ejecutar servicios a través del ESB
@app.route('/executeService', methods=['POST'])
def execute_esb_service():
    """
    No es necesario el docstring completo de Flasgger aquí si usamos flask_swagger_ui.
    La documentación se carga desde openapi.yaml
    """
    service_data = request.json
    if not service_data:
        return jsonify({"status": "error", "message": "Request body must be JSON."}), 400

    sys_service_id = service_data.get('SYSServiceID')
    if not sys_service_id:
        return jsonify({"status": "error", "message": "SYSServiceID is required in service_data."}), 400

    config = SERVICE_ID_TO_CONFIG_MAP.get(sys_service_id)
    if not config:
        return jsonify({"status": "error", "message": f"SYSServiceID '{sys_service_id}' no es una operación reconocida por el ESB."}), 404

    try:
        selected_class_reference = config['ref']
        selected_class_mapping = config['map']
        selected_service_properties = config['props']

        class_mapper = microesb.ClassMapper(
            class_references=selected_class_reference,
            class_mappings=selected_class_mapping,
            class_properties=selected_service_properties
        )

        esb_result_objects = microesb.ServiceExecuter().execute(
            class_mapper=class_mapper,
            service_data=service_data
        )

        final_response = {"status": "error", "message": "Formato de respuesta del ESB inesperado o nulo.", "raw_esb_output": str(esb_result_objects)}

        if esb_result_objects and isinstance(esb_result_objects, list) and len(esb_result_objects) > 0:
              # Acceder al primer ServiceMapper object
              service_mapper_instance = esb_result_objects[0]
              
              # Acceder al ClassMapper que está dentro del ServiceMapper
              # El ClassMapper (self._class_mapper) en ServiceMapper tiene las instancias de ClassHandler
              # como atributos (ej. ServiceMapper._class_mapper.Product)
              
              # Obtener el nombre del ClassHandler ejecutado para saber qué atributo buscar
              executed_handler_name = next(iter(service_data['data'][0])) # Ej: 'Product'

              # Obtener la instancia del ClassHandler
              # (Asumiendo que ServiceMapper._class_mapper es accesible y tiene el ClassHandler como atributo)
              class_handler_instance = getattr(service_mapper_instance._class_mapper, executed_handler_name, None)
              if class_handler_instance and hasattr(class_handler_instance, 'last_service_result') and class_handler_instance.last_service_result is not None:
                final_response = class_handler_instance.last_service_result
              else:
                final_response = {"status": "error", "message": "Resultado no encontrado en ClassHandler.", "raw_esb_output": str(esb_result_objects)}
            
        return jsonify(final_response), 200

    except Exception as e:
        print(f"Error procesando solicitud ESB: {e}")
        return jsonify({"status": "error", "message": f"Error interno del ESB: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)