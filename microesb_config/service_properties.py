# service_properties.py
service_properties_product = {
    'Product': {
        'properties': {
            'id': {'type': 'string', 'required': True, 'default': None},
            'nombre': {'type': 'string', 'required': False, 'default': None}, # Ahora puede ser opcional para update
            'descripcion': {'type': 'string', 'required': False, 'default': None},
            'categoria': {'type': 'string', 'required': False, 'default': None},
            'precio': {'type': 'float', 'required': False, 'default': None} # Usamos float aquí para la entrada, aunque internamente use Decimal
        },
        'methods': ['get_by_id', 'create', 'update', 'delete'] # Añadimos los nuevos métodos CRUD
    }
}

service_properties_messaging = {
    'MessagingService': { # Nueva entrada para el servicio de mensajería
        'properties': {
            'compra_data': {'type': 'dict', 'required': False, 'default': None}, # Para send_purchase_notification
            'log_data': {'type': 'dict', 'required': False, 'default': None}     # Para register_log_event
        },
        'methods': ['send_purchase_notification', 'register_log_event']
    }
}

service_properties_xls = {
    'ExcelCatalogoHandler': {
        'properties': {
            'product_id': {'type': 'string', 'required': False, 'default': None}, # Para get_by_id
            'nombre_parcial': {'type': 'string', 'required': False, 'default': None} # Para search_by_name
        },
        'methods': ['get_by_id', 'list_all', 'search_by_name']
    }
}

ALL_SERVICE_PROPERTIES = {
    'Product': service_properties_product,
    'MessagingService': service_properties_messaging,
    'ExcelCatalogoHandler': service_properties_xls
}