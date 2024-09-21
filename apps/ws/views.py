from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        self.accept()

    def websocket_receive(self, message):
        print('接收到消息', message)
        self.send(text_data='收到了')

    def websocket_disconnect(self, message):
        print('客户端断开连接了')
        raise StopConsumer()