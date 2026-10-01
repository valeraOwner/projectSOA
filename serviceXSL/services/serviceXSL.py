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
        
        # Validar extensión para usar el motor correcto si es necesario (pandas lo maneja bien)
        if not (filename.lower().endswith('.xls') or filename.lower().endswith('.xlsx')):
            raise ValueError("El archivo no es un formato XLS o XLSX válido.")

        xls_data = {}
        try:
            # sheet_name=None lee todas las hojas en un diccionario de DataFrames
            # pandas seleccionará el motor xlrd para .xls y openpyxl para .xlsx
            xls = pd.read_excel(filepath, sheet_name=None)
            
            for sheet_name, df in xls.items():
                # Convertir cada DataFrame (hoja) a JSON, orientado por registros (filas)
                # handle_nan_values=False evita que pandas convierta NaN a null si no lo quieres
                # Puedes ajustar to_dict(orient='records') a tus necesidades
                xls_data[sheet_name] = df.to_dict(orient='records')
                
            return json.dumps(xls_data, indent=2, ensure_ascii=False) # ensure_ascii para caracteres especiales
            
        except Exception as e:
            print(f"Error al convertir XLS/XLSX a JSON: {e}")
            raise # Re-lanza la excepción para que Flask la capture