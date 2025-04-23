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
    print(f"Sending (sync): {data}")
    try:
        record_metadata = producer.send(topic_name, value=data).get(timeout=10)
        print(f"✅ Sent to topic: {record_metadata.topic}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")
    except Exception as ex:
        print(f"❌ Error: {ex}")
    sleep(0.5)

producer.close()
