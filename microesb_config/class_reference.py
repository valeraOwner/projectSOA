# class_reference.py
class_reference_product = {
    'Product': {
        'property_ref': 'Product',
        'children': {}
    }
}
class_reference_messaging = {
    'MessagingService': { 
        'property_ref': 'MessagingService',
        'children': {}
    }
}
class_reference_xls = {
    'ExcelCatalogoHandler': {
        'property_ref': 'ExcelCatalogoHandler',
        'children': {}
    }
}

# Puedes mantener un diccionario consolidado para fácil acceso si quieres,
# pero el ClassMapper se creará con uno de los individuales.
ALL_CLASS_REFERENCES = {
    'Product': class_reference_product,
    'MessagingService': class_reference_messaging,
    'ExcelCatalogoHandler': class_reference_xls
}