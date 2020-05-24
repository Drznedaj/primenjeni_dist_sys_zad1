from kazoo.client import KazooClient, KazooState, DataWatch, ChildrenWatch
from kazoo.exceptions import NodeExistsError
import logging
from time import sleep
from random import randint
from collections import defaultdict

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
vote = None
try:
    try:
        leader_node = '/leader'
        votes_node = '/votes'
        poll = defaultdict(int)
        zk.create(leader_node, value=b'start', ephemeral=True)
        print('I am the Leader!!!')
        print('Start voting!')
        #zk.set(leader_node, b'start')

        @ChildrenWatch(zk, votes_node)
        def my_func(children):
            print(f"Children are {children}")
            if len(children) == 3:
                for child in children:
                    vote = zk.get(votes_node+'/'+child)
                    print(f'Node: {child} voted: {vote[0].decode()}')
                    poll[vote[0].decode()] += 1

                won_poll = 'ya' if poll['ya'] > poll['no'] else 'no'
                print(f'Poll result is: {won_poll}')
                zk.set(leader_node, won_poll.encode())

    except NodeExistsError:
        print('Leader already set, whatching out for it...')

        @DataWatch(zk, leader_node)
        def my_func(data, stat, event):
            print("Data is %s" % data)
            global vote
            if data == b'start':
                print('Voting...')
                random_vote = 'ya' if randint(0, 1) == 1 else 'no'
                vote = random_vote
                zk.create(votes_node+'/vote', value=random_vote.encode(), ephemeral=True, sequence=True)
            elif data != None and vote != None:
                result = 'won' if vote == data.decode() else 'lost'
                print(f'{zk.client_id[0]}: My vote {result}!')
    sleep(100)
except KeyboardInterrupt:
    pass

zk.stop()
