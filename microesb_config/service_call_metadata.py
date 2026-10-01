# service_call_metadata.py
"=============== DB =================="
service_metadata = {
    'SYSServiceID': 'getProductById',
    'data': [
        {
            'Product': {
                'SYSServiceMethod': 'get_by_id',
                'id': 'P001'
            }
        }
    ]
}

service_metadata_create = {
    'SYSServiceID': 'createProduct',
    'data': [
        {
            'Product': {
                'SYSServiceMethod': 'create',
                'id': 'P005',
                'nombre': 'Auriculares Bluetooth',
                'descripcion': 'Auriculares inalámbricos con cancelación de ruido',
                'categoria': 'Audio',
                'precio': 99.99
            }
        }
    ]
}

service_metadata_update = {
    'SYSServiceID': 'updateProductById',
    'data': [
        {
            'Product': {
                'SYSServiceMethod': 'update',
                'id': 'P005',
                'precio': 109.99, # Solo actualizamos el precio
                'descripcion': 'Auriculares inalámbricos con sonido HD' # Y la descripción
            }
        }
    ]
}

service_metadata_delete = {
    'SYSServiceID': 'deleteProductById',
    'data': [
        {
            'Product': {
                'SYSServiceMethod': 'delete',
                'id': 'P005'
            }
        }
    ]
}

"=============== MENSAJERIA =================="

service_metadata_send_purchase = {
    'SYSServiceID': 'sendPurchaseNotificacion', 
    'data': [
        {
            'MessagingService': {
                'SYSServiceMethod': 'send_purchase_notification',
                'compra_data': {
                    "order_id": "ORD002",
                    "product_id": "P003",
                    "quantity": 1,
                    "customer_email": "otro@example.com",
                    "timestamp": "2025-06-21T10:30:00Z"
                }
            }
        }
    ]
}

service_metadata_register_log = {
    'SYSServiceID': 'registerLogEvent',
    'data': [
        {
            'MessagingService': {
                'SYSServiceMethod': 'register_log_event',
                'log_data': {
                    "level": "WARNING",
                    "message": "Intento de acceso fallido desde IP 192.168.1.10.",
                    "service": "security",
                    "timestamp": "2025-06-21T10:35:00Z"
                }
            }
        }
    ]
}

"=============== SERVICIO HANDLING XLS =================="

service_metadata_xls_get_by_id = {
    'SYSServiceID': 'getById',
    'data': [
        {
            'ExcelCatalogoHandler': {
                'SYSServiceMethod': 'get_by_id',
                'product_id': 'EL001' 
            }
        }
    ]
}

service_metadata_xls_list_all = {
    'SYSServiceID': 'listAll',
    'data': [
        {
            'ExcelCatalogoHandler': {
                'SYSServiceMethod': 'list_all_products'
                # No se necesitan datos adicionales
            }
        }
    ]
}

service_metadata_xls_search_by_name = {
    'SYSServiceID': 'searchByName',
    'data': [
        {
            'ExcelCatalogoHandler': {
                'SYSServiceMethod': 'search_products_by_name',
                'nombre_parcial': 'Cable'
            }
        }
    ]
}