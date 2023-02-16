import asyncio

from aiokafka import AIOKafkaProducer

from app.core.config import settings


def get_kafka_producer() -> AIOKafkaProducer:
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        loop=loop,
    )
    return producer


async def start_kafka() -> None:  # pragma: no cover
    """
    Start kafka producer.
    """
    kafka_producer = get_kafka_producer()
    kafka_producer.start()


async def shutdown_kafka() -> None:  # pragma: no cover
    """
    Shutdown kafka client.
    """
    kafka_producer = get_kafka_producer()
    kafka_producer.stop()
