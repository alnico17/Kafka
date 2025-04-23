from json import dumps
from kafka import KafkaProducer
from time import sleep

topic_name = 'hello_world1'

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

for e in range(10):
    data = {'number': e}
    print(f"Sending (fire-and-forget): {data}")
    producer.send(topic_name, value=data)
    sleep(0.5)

producer.close()
