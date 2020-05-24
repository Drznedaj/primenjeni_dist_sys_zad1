from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NodeExistsError
import logging
from time import sleep

logging.basicConfig()


def my_listener(state):
    if state == KazooState.LOST:
        print('Lost')  # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        print('Suspended')  # Handle being disconnected from Zookeeper
    else:
        print('Connected')  # Handle being connected/reconnected to Zookeeper


zk = KazooClient(hosts='127.0.0.1:2181')
zk.add_listener(my_listener)

zk.start()
try:
    try:
        zk.create('/leader', ephemeral=True)
    except NodeExistsError:
        print('Leader already set, whatching out for it...')
    sleep(5)
except KeyboardInterrupt:
    pass

zk.stop()
