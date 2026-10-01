# services/excel_catalogo_handler.py (Nuevo archivo)
import json
from microesb import microesb
from .xsl_service import CatalogoXLSService # Asegúrate de que esta ruta sea correcta

class ExcelCatalogoHandler(microesb.ClassHandler):
    def __init__(self):
        super().__init__()
        # Verificar la ruta del archivo y el directorio
        self.xls_service = CatalogoXLSService(filename="catalog.xls", data_dir="data", hoja="Catalog")
        self.last_service_result = None # <-- ¡AÑADIR ESTO! Inicializarlo a None
        print("ExcelCatalogoHandler inicializado y xls_service cargado.")

    def get_by_id(self):
        """
        Recupera los detalles de un producto por su ID del catálogo XLS.
        El 'product_id' es inyectado por el ESB.
        """
        if not hasattr(self, 'product_id'):
            return {"status": "error", "message": "Parámetro 'product_id' no proporcionado."}
        
        result = self.xls_service.obtener_producto_por_id(self.product_id)
        #print(json.dumps(result, indent=2, ensure_ascii=False))
        # El xsl_service ya devuelve un diccionario con 'status' y 'message'/'producto'
        self.last_service_result = result # <-- ¡GUARDAR EL RESULTADO AQUÍ!
        return result

    def list_all_products(self):
        """
        Devuelve una lista de todos los productos del catálogo XLS.
        """
        result = self.xls_service.listar_todos_productos()
        #print(json.dumps(result, indent=2, ensure_ascii=False))
        self.last_service_result = result # <-- ¡GUARDAR EL RESULTADO AQUÍ!
        return result

    def search_products_by_name(self):
        """
        Busca productos cuyo nombre contenga una cadena específica en el catálogo XLS.
        El 'nombre_parcial' es inyectado por el ESB.
        """
        if not hasattr(self, 'nombre_parcial'):
            return {"status": "error", "message": "Parámetro 'nombre_parcial' no proporcionado."}
        
        result = self.xls_service.buscar_productos_por_nombre(self.nombre_parcial)
        #print(json.dumps(result, indent=2, ensure_ascii=False))
        self.last_service_result = result # <-- ¡GUARDAR EL RESULTADO AQUÍ!
        return result