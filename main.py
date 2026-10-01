# main.py
from microesb import microesb
from microesb_config.service_properties import *
from microesb_config.class_reference import *
from microesb_config.class_mapping import *

from microesb_config.service_call_metadata import *

class_mapper_product = microesb.ClassMapper(
    class_references=class_reference_product,
    class_mappings=class_mapping_product,
    class_properties=service_properties_product
)

class_mapper_messaging = microesb.ClassMapper(
    class_references=class_reference_messaging,
    class_mappings=class_mapping_messaging,
    class_properties=service_properties_messaging
)

class_mapper_xls = microesb.ClassMapper(
    class_references=class_reference_xls,
    class_mappings=class_mapping_xls,
    class_properties=service_properties_xls
)

# --- PRUEBA 1: CREAR PRODUCTO ---
print("\n--- Probando CREAR PRODUCTO ---")
result_create = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_product,
    service_data=service_metadata_create
)
print(result_create)

# --- PRUEBA 2: OBTENER PRODUCTO RECIÉN CREADO ---
print("\n--- Probando OBTENER PRODUCTO CREADO (P005) ---")
# Modifica service_metadata para pedir P005
service_metadata_get_p005 = {
    'SYSServiceID': 'getProductById',
    'data': [
        {
            'Product': {
                'SYSServiceMethod': 'get_by_id',
                'id': 'P005'
            }
        }
    ]
}
result_get_p005 = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_product,
    service_data=service_metadata_get_p005
)
print(result_get_p005)

# --- PRUEBA 3: ACTUALIZAR PRODUCTO ---
print("\n--- Probando ACTUALIZAR PRODUCTO (P005) ---")
result_update = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_product,
    service_data=service_metadata_update
)
print(result_update)

# --- PRUEBA 4: OBTENER PRODUCTO ACTUALIZADO ---
print("\n--- Probando OBTENER PRODUCTO ACTUALIZADO (P005) ---")
result_get_updated_p005 = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_product,
    service_data=service_metadata_get_p005
)
print(result_get_updated_p005)

# --- PRUEBA 5: ELIMINAR PRODUCTO ---
print("\n--- Probando ELIMINAR PRODUCTO (P005) ---")
result_delete = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_product,
    service_data=service_metadata_delete
)
print(result_delete)


# --- PRUEBA 6: INTENTAR OBTENER PRODUCTO ELIMINADO ---
print("\n--- Probando OBTENER PRODUCTO ELIMINADO (P005) ---")
result_get_deleted_p005 = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_product,
    service_data=service_metadata_get_p005
)
print(result_get_deleted_p005)

# --- PRUEBA 7: ENVIAR NOTIFICACIÓN DE COMPRA ---
print("\n--- Probando ENVIAR NOTIFICACIÓN DE COMPRA ---")
result_send_purchase = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_messaging,
    service_data=service_metadata_send_purchase
)
print(result_send_purchase)

# --- PRUEBA 8: REGISTRAR EVENTO DE LOG ---
print("\n--- Probando REGISTRAR EVENTO DE LOG ---")
result_register_log = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_messaging,
    service_data=service_metadata_register_log
)
print(result_register_log)

# --- PRUEBA 9: OBTENER PRODUCTO DE XLS POR ID ---
print("\n--- Probando OBTENER PRODUCTO DE XLS POR ID (ID EL001) ---")
result_xls_get = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_xls,
    service_data=service_metadata_xls_get_by_id
)
print(result_xls_get)

# --- PRUEBA 10: LISTAR TODOS LOS PRODUCTOS DE XLS ---
print("\n--- Probando LISTAR TODOS LOS PRODUCTOS DE XLS ---")
result_xls_list = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_xls,
    service_data=service_metadata_xls_list_all
)
print(result_xls_list)

# --- PRUEBA 11: BUSCAR PRODUCTOS EN XLS POR NOMBRE ---
print("\n--- Probando BUSCAR PRODUCTOS EN XLS POR NOMBRE ('Cable') ---")
result_xls_search = microesb.ServiceExecuter().execute(
    class_mapper=class_mapper_xls,
    service_data=service_metadata_xls_search_by_name
)
print(result_xls_search)