# messaging_service/rabbitmq_service.py
import amqpstorm
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rabbitmq_config import RABBITMQ_CONFIG, QUEUE_NAMES

class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None

    def _get_channel(self):
        """Establece y devuleve un canal de RabbitMQ"""
        if self.connection is None or not self.connection.is_open:
            try:
                self.connection = amqpstorm.Connection(
                    RABBITMQ_CONFIG["host"],
                    RABBITMQ_CONFIG["login"],
                    RABBITMQ_CONFIG["password"],
                    port=RABBITMQ_CONFIG["port"],
                    virtual_host=RABBITMQ_CONFIG["virtual_host"]
                )
                print("Conexion a RabbitMQ establecida.")
            except amqpstorm.AMQPConnectionError as e:
                print(f"Error al conectar a RabbitMQ: {e}")
                self.connection = None
                return None
            
        if self.channel is None or not self.channel.is_open:
            try:
                self.channel = self.connection.channel()
                # Declarar cola para asegurar que existe
                self.channel.queue.declare(queue=QUEUE_NAMES["notifications"], durable=True)
                self.channel.queue.declare(queue=QUEUE_NAMES["logs"], durable=True)
                print("Canal de RabbitMQ establecido y colas declaradas")
            except amqpstorm.AMQPChannelError as e:
                print(f"Error al abrir canal o declarar colas: {e}")
                self.channel = None
        return self.channel 
    
    def _close_channel_and_connection(self):
        """Cierra el canal y la conexion de RabbitMQ"""
        if self.channel and self.channel.is_open:
            try:
                self.channel.close()
                print("Canal de RabbitMQ cerrado.")
            except Exception as e:
                print(f"Error al cerrar el canal: {e}")
            finally:
                self.channel = None
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
                print("Conexion a RabbitMQ cerrada.")
            except Exception as e:
                print(f"Error al cerrar la conexion: {e}")
            finally:
                self.connection = None
        
    def enviar_notificacion_compra(self, compra_data):
        """
        Publica un mensaje en la cola de notificaciones de compra
        """
        channel = self._get_channel()
        if not channel:
            return {"status": "error", "message": "No se pudo obtener el canal de RabbitMQ"}        
        
        try:
            message_body = json.dumps(compra_data)
            properties = {
                'content_type': 'application/json',
                'delivery_mode': 2 # para mensaje persistente
            }
            channel.basic.publish(
                body=message_body,
                routing_key=QUEUE_NAMES["notifications"],
                properties=properties
            )
            print(f"Mensaje de compra enviado a '{QUEUE_NAMES['notifications']}': {message_body}")
            return {"status": "success", "message": "Notificacion de compra enviada."}
        except Exception as e:
            print(f"Error al publicar notificacion de compra: {e}")
            return {"status": "error", "message": f"Error al enviar notificacion de compra: {e}"}
        finally:
            pass
    
    def registrar_evento_log(self, log_data):
        """
        Publica un mensaje en la cola de logs
        """
        channel = self._get_channel()
        if not channel:
            return {"status": "error", "message": "No se pudo obtener el canal de RabbitMQ"}        

        try:
            message_body = json.dumps(log_data)
            properties = {
                'content_type': 'application/json',
                'delivery_mode': 2 # para mensaje persistente
            }
            channel.basic.publish(
                body=message_body,
                routing_key=QUEUE_NAMES["logs"],
                properties=properties
            )
            print(f"Mensaje de log enviado a '{QUEUE_NAMES['logs']}': {message_body}")
            return {"status": "success", "message": "Evento de log registrado."}
        except Exception as e:
            print(f"Error al publicar evento de log: {e}")
            return {"status": "error", "message": f"Error al enviar evento de log: {e}"}
        finally:
            pass

if __name__ == "__main__":
    mq_service = RabbitMQService()

    print("\n--- Probando enviar Notificacion de Compra ---")
    compra_info = {
        "order_id": "ORD001",
        "product_id": "P001",
        "quantity": 2,
        "customer_email": "cliente@example.com",
        "timestamp": "2025-06-21T10:00:00Z"
    }

    result_compra = mq_service.enviar_notificacion_compra(compra_data=compra_info)
    print(result_compra)

    print("\n--- Probando Registrar Evento de Log ---")
    log_info = {
        "level": "INFO",
        "message": "Usuario P001 ha iniciado sesión.",
        "service": "auth_service",
        "timestamp": "2025-06-21T10:01:00Z"
    }
    result_log = mq_service.registrar_evento_log(log_info)
    print(result_log)

    # Asegurarse de cerrar la conexion al finalizar las pruebas
    mq_service._close_channel_and_connection()

    print("\nIntenta acceder a http://localhost:15672/ para ver las colas y mensajes (user/password)")