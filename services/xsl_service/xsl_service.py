# PROJECTSOA/services/serviceXSL.py

import pandas as pd
import json
import os

class XLStoJSONConverter:
    """
    Clase que encapsula la lógica para convertir archivos XLS/XLSX a JSON.
    """
    def __init__(self, data_dir="data"):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # /app/services
        self.data_dir = os.path.join(os.path.dirname(base_dir), data_dir)  # /app/data
        print(f"XLStoJSONConverter inicializado. Directorio de datos: {self.data_dir}")

    def process_xls_file(self, filename: str) -> str:
        """
        Lee un archivo XLS/XLSX y lo convierte a una cadena JSON.
        Cada hoja se convierte en una entrada en el diccionario JSON,
        y cada hoja es una lista de diccionarios (registros/filas).
        """
        filepath = os.path.join(self.data_dir, filename)
        print(f"[DEBUG] Ruta completa del archivo: {filepath}")  # <-- importante
        
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Archivo XLS/XLSX no encontrado en {filepath}")
        
        if not (filename.lower().endswith('.xls') or filename.lower().endswith('.xlsx')):
            raise ValueError("El archivo no es un formato XLS o XLSX válido.")

        xls_data = {}
        try:
            xls = pd.read_excel(filepath, sheet_name=None)
            for sheet_name, df in xls.items():
                xls_data[sheet_name] = df.to_dict(orient='records')
            return json.dumps(xls_data, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al convertir XLS/XLSX a JSON: {e}")
            raise

class CatalogoXLSService:
    """
    Servicio para interactuar con el catálogo de productos en un archivo Excel.
    """
    def __init__(self, filename="catalog.xls", data_dir="data", hoja="Productos"):
        # Usa la ruta absoluta desde la raíz del proyecto
        self.filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", data_dir, filename
        ))
        self.hoja = hoja
        #print(f"Buscando archivo en: {self.filepath}")
        print(f"CatalogoXLSService inicializado. Archivo: {self.filepath}")

    def _cargar_catalogo(self):
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"Archivo de catálogo no encontrado en {self.filepath}")
        try:
            df = pd.read_excel(self.filepath, sheet_name=self.hoja)
            return df
        except Exception as e:
            print(f"Error al leer el catálogo XLS: {e}")
            raise

    def obtener_producto_por_id(self, product_id):
        """
        Recupera los detalles de un producto por su ID.
        """
        try:
            df = self._cargar_catalogo()
            producto = df[df['ProductID'] == product_id]
            if producto.empty:
                return {"status": "error", "message": f"Producto con id '{product_id}' no encontrado."}
            return {"status": "success", "producto": producto.iloc[0].to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def listar_todos_productos(self):
        """
        Devuelve una lista de todos los productos del catálogo.
        """
        try:
            df = self._cargar_catalogo()
            productos = df.to_dict(orient='records')

            #print(f"Productos disponibles:\n {productos}")

            return {"status": "success", "productos": productos}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def buscar_productos_por_nombre(self, nombre_parcial):
        """
        Busca productos cuyo nombre contenga una cadena específica.
        """
        try:
            df = self._cargar_catalogo()
            productos = df[df['ProductName'].str.contains(nombre_parcial, case=False, na=False)]

            #print(f"Productos encontrados con el nombre {nombre_parcial}: {productos}")

            if productos.empty:
                return {"status": "success", "productos": []}
            return {"status": "success", "productos": productos.to_dict(orient='records')}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Pruebas rápidas
    catalogo = CatalogoXLSService(filename="catalog.xls", data_dir="data", hoja="Catalog")

    print("\n--- Listar todos los productos ---")
    print(json.dumps(catalogo.listar_todos_productos(), indent=2, ensure_ascii=False))

    print("\n--- Obtener producto por ID ---")
    print(json.dumps(catalogo.obtener_producto_por_id(product_id='EL001'), indent=2, ensure_ascii=False))

    print("\n--- Buscar productos por nombre ---")
    print(json.dumps(catalogo.buscar_productos_por_nombre(nombre_parcial="Cable"), indent=2, ensure_ascii=False))