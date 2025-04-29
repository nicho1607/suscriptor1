from services.subscriber_service import SubscriberService

if __name__ == "__main__":
    print("Iniciando suscriptor para guardar en base de datos...")
    subscriber = SubscriberService()
    subscriber.start_consuming()