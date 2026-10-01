# rabbitmq_config.py

# Configuración de conexión a RabbitMQ
RABBITMQ_CONFIG = {
    "host": "localhost",  # O el nombre del servicio Docker si se llama desde otro contenedor (ej. 'rabbitmq')
    "port": 5672,
    "login": "user",
    "password": "password",
    "virtual_host": "/" # Virtual host por defecto
}

# Nombre para la cola
QUEUE_NAMES = {
    "notifications": "notifications_queue",
    "logs": "logs_queue"
}