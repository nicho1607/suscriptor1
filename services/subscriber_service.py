import pika
from config.rabbitmq_config import RabbitMQConfig
from domain.models import PreInscripcion
from infrastructure.repository import PreInscripcionRepository

class SubscriberService:
    def __init__(self):
        self.rabbit_config = RabbitMQConfig()
        self.repository = PreInscripcionRepository()
        
    def callback(self, ch, method, properties, body):
        try:
            pre_inscripcion = PreInscripcion.from_json(body.decode())
            success, message = self.repository.save(pre_inscripcion)
            
            if success:
                print(f" [x] Guardado en DB: {pre_inscripcion}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print(f" [x] Error al guardar: {message}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                
        except Exception as e:
            print(f" [x] Error procesando mensaje: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
    def start_consuming(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbit_config.host,
                port=self.rabbit_config.port,
                virtual_host=self.rabbit_config.virtual_host,
                credentials=self.rabbit_config.credentials
            )
        )
        
        channel = connection.channel()
        channel.exchange_declare(
            exchange=self.rabbit_config.exchange,
            exchange_type='topic',
            durable=True
        )
        
        channel.queue_declare(
            queue=self.rabbit_config.queue_name,
            durable=True,
            exclusive=False
        )
        
        channel.queue_bind(
            exchange=self.rabbit_config.exchange,
            queue=self.rabbit_config.queue_name,
            routing_key=self.rabbit_config.routing_key
        )
        
        print(' [*] Esperando mensajes. Para salir presione CTRL+C')
        
        channel.basic_consume(
            queue=self.rabbit_config.queue_name,
            on_message_callback=self.callback,
            auto_ack=False
        )
        
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print(" [*] Cerrando conexión...")
            connection.close()