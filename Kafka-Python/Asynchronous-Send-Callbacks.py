from json import dumps
from kafka import KafkaProducer
from time import sleep

topic_name = 'hello_world1'

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def on_send_success(record_metadata, message):
    print(f"""✅ Success:
    ➤ Message: {message}
    ➤ Topic: {record_metadata.topic}
    ➤ Partition: {record_metadata.partition}
    ➤ Offset: {record_metadata.offset}
    """)

def on_send_error(excp, message):
    print(f"❌ Failed to send {message}, Error: {excp}")

for e in range(10):
    data = {'number': e}
    print(f"Sending (async): {data}")
    producer.send(topic_name, value=data) \
        .add_callback(on_send_success, message=data) \
        .add_errback(on_send_error, message=data)
    sleep(0.5)

producer.flush()
producer.close()
