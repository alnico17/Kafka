# Producer Code:
# ------------------------------------
from time import sleep
from json import dumps
from kafka import KafkaProducer

topic_name='hello_world4'
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'number' : e}
    print(data)
    producer.send(topic_name, value=data)
    sleep(2)

# Consumer Code:
# ---------------------------------------
from kafka import KafkaConsumer


import json


consumer = KafkaConsumer ('hello_world4',bootstrap_servers = ['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('utf-8')),group_id='demo112215sgtrjwrykvjh',auto_offset_reset='earliest')


for message in consumer:
    print(message)
