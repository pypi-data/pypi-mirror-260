import logging
import time

from stompypy import Listener
from stompypy import Stomp


class MyListener(Listener):
    def on_disconnect(self):
        print('Disconnected ')

    def on_connect(self):
        print('Connected')

    def on_message(self, frame) -> None:
        print('Message:', frame.body)


if __name__ == '__main__':
    logger = logging.getLogger('stompypy')
    logger.setLevel(logging.DEBUG)

    # Create a STOMP connection to the server
    # connection = Stomp.create_connection(host='toad.rmq.cloudamqp.com', port=61614, use_ssl=True)
    connection = Stomp.create_connection(
        host='localhost',
        port=61614,
        use_ssl=True,
        cafile='/Users/hugobrilhante/Developer/Repos/stompypy/rabbitmq/certs/rabbitmq.crt',
    )

    # Add listener
    connection.add_listener(MyListener())

    # Connect to the STOMP server
    # connection.connect(host='svaitpts', login='svaitpts', passcode='DiiF9qGxhetlPQbtijHvYlYtv3L8Kezd')
    connection.connect(heartbeat=(5000, int(5000*1.5)))

    # Subscribe to a destination
    connection.subscribe(id='1', destination='/queue/example', ack_mode='auto')

    # Send a message to the destination
    connection.send(destination='/queue/example', content_type='text/plain', body='Hello World!')

    time.sleep(60)

    # Disconnect from the server
    connection.disconnect()
