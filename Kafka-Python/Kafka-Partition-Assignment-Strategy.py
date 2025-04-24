# Producer Code:
# ---------------------
from time import sleep
from json import dumps
from kafka import KafkaProducer


def custom_partitioner(key, all_partitions, available):
    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """
    print("The key is  : {}".format(key))
    print("All partitions : {}".format(all_partitions))
    print("After decoding of the key : {}".format(key.decode('UTF-8')))
    return int(key.decode('UTF-8'))%len(all_partitions)


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'),partitioner=custom_partitioner)
topic_name='hello_world'

for e in range(0,100):
    data={"number":e}
    producer.send(topic_name, key=str(e).encode(), value=data)
    sleep(1)
 
# Consumer Code:
# ----------------------
from kafka.coordinator.assignors.range import RangePartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata
import kafka

import json

class MyConsumerRebalanceListener(kafka.ConsumerRebalanceListener):


    def on_partitions_revoked(self, revoked):
        print("Partitions %s revoked" % revoked)
        print('*' * 50)

    def on_partitions_assigned(self, assigned):
        print("Partitions %s assigned" % assigned)
        print('*' * 50)

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         group_id='demo112215sgtrjwrykvjh', auto_offset_reset='earliest',
                         enable_auto_commit=False,partition_assignment_strategy=[RoundRobinPartitionAssignor])

listener = MyConsumerRebalanceListener()
consumer.subscribe('hello_world',listener=listener)



for message in consumer:
    print(message)
    print("The value is : {}".format(message.value))
    tp=TopicPartition(message.topic,message.partition)
    om = OffsetAndMetadata(message.offset+1, message.timestamp)
    consumer.commit({tp:om})