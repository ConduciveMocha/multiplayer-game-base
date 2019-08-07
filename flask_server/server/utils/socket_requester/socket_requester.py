import socketio
import sys
class SocketRequester:
    def __init__(self,url='http://localhost:5000',namespaces=None):
        self._url = url
        self.namespaces = namespaces if namespaces else []
        self.sio = socketio.Client()
    
        @self.sio.on('connect')
        def on_connect():
            print('Connected')
        @self.sio.on('NEW_MESSAGE', namespace='/message')
        def new_message(data):
            print(data)
        self.sio.connect(url)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self,new_url):
        if self._url == new_url:
            return
        else:
            self.sio.disconnect()
            self.sio.connect(new_url, namespaces=self.namespaces)

    def emit_event(self,event,data,namespace):
        self.sio.emit(event, data, namespace=namespace)
    def disconnect(self):
        if self.sio:
            print('Disconnecting')
            self.sio.disconnect()
            self.sio = None

    def __delete__(self,instance):
        self.disconnect()


s = SocketRequester(namespaces=['/message'])
s2 = SocketRequester(namespaces=['/message'])
s.emit_event('SEND_MESSAGE', {'content':'message1', 'thread':15,'sender':2}, '/message')
s.emit_event('SEND_MESSAGE', {'content':'message2', 'thread':15,'sender':2}, '/message')
s2.emit_event('SEND_MESSAGE', {'content':'message3','thread':15,'sender':3}, '/message')