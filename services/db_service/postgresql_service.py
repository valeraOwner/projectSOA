# service/postgresql_service.py

from decimal import Decimal
import psycopg2

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_config import DB_CONFIG

class PostgreSQLService:
    def __init__(self):
        self.conn = None

    def _get_connection(self):
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(**DB_CONFIG)
                print("Conexión a la base de datos PostgreSQL establecida.")
            except psycopg2.Error as e:
                print(f'Error al conectar a la base de datos PostgreSQL: {e}')
                self.conn = None # Asegurarse de que conn sea None en caso de error
        return self.conn

    def _close_connection(self):
        """Cierra la conexión a la base de datos PostgreSQL si está abierta."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None
            print("Conexión a la base de datos PostgreSQL cerrada.")

    def obtener_producto_db_por_id(self, product_id):
        """
        Obtiene un producto de la base de datos PostgreSQL por su ID.
        """
        conn = self._get_connection()
        if not conn:
            return {"status": "error", "message": "No se pudo establecer la conexión a la base de datos."}
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre, descripcion, categoria, precio FROM productos WHERE id = %s", (product_id,))
                producto = cursor.fetchone()

                if producto:
                    # Mapea el resultado a un diccionario
                    columns = [desc[0] for desc in cursor.description]
                    return {"status": "success", "producto": dict(zip(columns, producto))}
                else:
                    return {"status": "error", "message": f"Producto con ID {product_id} no encontrado."}
        except psycopg2.Error as e:
            # Revertir cambios en caso de error
            conn.rollback()
            return {"status": "error", "message": f"Error al obtener el producto: {e}"}
        finally:
            # Opcionalmente cerrar la conexión
            #self._close_connection()
            pass

    def crear_producto(self, id, nombre, descripcion, categoria, precio):
        """
        Insertar un nuevo producto en la tabla de PostgreSQL
        """
        conn = self._get_connection()
        if not conn:
            return {"status": "error", "message": "No se pudo establecer la conexión a la base de datos."}
        
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO productos (id, nombre, descripcion, categoria, precio) VALUES (%s, %s, %s, %s, %s);",
                    (id, nombre, descripcion, categoria, Decimal(str(precio))) # Asegura que el precio sea Decimal
                )
                conn.commit() # Confirmar la transacción
                return {"status": "success", "message": f"Producto {nombre} (ID: {id}) creado exitosamente."}
        except psycopg2.IntegrityError as e: # Manejar error de clave duplicada
            conn.rollback()
            return {"status": "error", "message": f"Error de integridad: El producto con ID {id} ya existe. {e}"}
        except psycopg2.Error as e:
            conn.rollback()
            return {"status": "error", "message": f"Error al crear producto: {e}"}
        finally:
            pass
    
    def actualizar_producto(self, id, nombre=None, descripcion=None, categoria=None, precio=None):
        """
        Actualiza los detalles de un producto existente en la base de datos
        Se permite una actualizacion parcial
        """
        conn = self._get_connection()
        if not conn:
            return {"status": "error", "message": "No se pudo establecer la conexión a la base de datos."}
        
        updates = []
        params = []
        if nombre is not None:
            updates.append("nombre = %s")
            params.append(nombre)
        if descripcion is not None:
            updates.append("descripcion = %s")
            params.append(descripcion)
        if categoria is not None:
            updates.append("categoria = %s")
            params.append(categoria)
        if precio is not None:
            updates.append("precio = %s")
            params.append(Decimal(str(precio)))

        if not updates:
            return {"status": "error", "messages": "No se proporcionaron campos para actualizar"}
        
        params.append(id) # ID al final de WHERE
        query = f"UPDATE productos SET {', '.join(updates)} WHERE id = %s;"

        try:
            with conn.cursor() as cur:
                cur.execute(query, tuple(params))
                if cur.rowcount == 0:
                    conn.rollback()
                    return {"status": "error", "message": f"Producto con ID {id} no encontrado para actualizar"}
                conn.commit()
                return {"status": "success", "message": f"Producto con ID {id} actualizado exitosamente."}
        except psycopg2.Error as e:
            conn.rollback()
            return{"status": "error", "message": f"Error al actualizar producto: {e}"}
        finally:
            pass
    
    def eliminar_producto(self, id):
        """
        Elimina un producto de la base de datos por su ID.
        """
        conn = self._get_connection()
        if not conn:
            return {"status": "error", "message": "No se pudo conectar a la base de datos."}

        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM productos WHERE id = %s;", (id,))
                if cur.rowcount == 0:
                    conn.rollback()
                    return {"status": "error", "message": f"Producto con ID {id} no encontrado para eliminar."}
                conn.commit()
                return {"status": "success", "message": f"Producto con ID {id} eliminado exitosamente."}
        except psycopg2.Error as e:
            conn.rollback()
            return {"status": "error", "message": f"Error al eliminar producto: {e}"}
        finally:
            pass

if __name__ == "__main__":
    db_service = PostgreSQLService()
    
    # Probar crear producto
    print("\n--- Probando Crear Producto ---")
    new_product = db_service.crear_producto("P004", "Monitor Curvo", "Monitor ultrawide 34 pulgadas", "Monitores", 450.00)
    print(new_product)
    new_product2 = db_service.crear_producto("P001", "Laptop Gamer Duplicada", "Esto debería fallar", "Laptops", 100.00)
    print(new_product2) # Debería dar error de duplicado

    # Probar obtener producto
    print("\n--- Probando Obtener Producto ---")
    prod_existente = db_service.obtener_producto_db_por_id("P004")
    print(prod_existente)

    # Probar actualizar producto
    print("\n--- Probando Actualizar Producto ---")
    update_result = db_service.actualizar_producto("P004", precio=499.99, categoria="Pantallas")
    print(update_result)
    updated_prod = db_service.obtener_producto_db_por_id("P004")
    print(updated_prod)

    # Probar eliminar producto
    print("\n--- Probando Eliminar Producto ---")
    delete_result = db_service.eliminar_producto("P004")
    print(delete_result)
    deleted_prod = db_service.obtener_producto_db_por_id("P004")
    print(deleted_prod) # Debería decir que no se encontró

    db_service._close_connection()  # Cerrar la conexión al final