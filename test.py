from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.client import KeeperState

import logging
logging.basicConfig()


log = logging.getLogger()
log.setLevel('DEBUG')

zk = KazooClient(hosts='127.0.0.1:2181')
# zk.start()
# zk.stop()
from kazoo.client import KazooState

def my_listener(state):
    if state == KazooState.LOST:
        logging.warning('Lost')
    elif state == KazooState.SUSPENDED:
        logging.warning('Suspend')
    else:
        logging.warning('else')



zk.add_listener(my_listener)

@zk.add_listener
def watch_for_ro(state):
    if state == KazooState.CONNECTED:
        if zk.client_state == KeeperState.CONNECTED_RO:
            print("Read only mode!")
        else:
            print("Read/Write mode!")

zk.start()
zk.ensure_path("/my/newoff")
# zk.create("/my/new/node", b"a value")
#
# if zk.exists("/my/favorite"):
#     print('vova')
zk.set("/my/newoff", b"some aad")
data, stat = zk.get("/my/newoff")
print(data.decode("utf-8"))

# zk.stop()
