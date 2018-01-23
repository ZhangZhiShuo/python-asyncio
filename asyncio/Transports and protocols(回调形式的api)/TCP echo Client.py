import asyncio
class TCPEchoClientProtocol(asyncio.Protocol):
      def __init__(self,message,loop):
          self.message=message
          self.loop=loop
          self.transport=None
      def connection_made(self, transport):
          print(transport)
          self.transport=transport
          transport.write(self.message.encode())
          print('Data sent:{!r}'.format(self.message))
      def data_received(self, data):
          print('Data received:{!r}'.format(data.decode()))
          #self.transport.close()
      def connection_lost(self, exc):
          print("The connection  is closed",self.transport)
          print('Stop the event loop')
          self.loop.stop()
if __name__=="__main__":
    loop=asyncio.get_event_loop()
    message="Hello world"
    coro=loop.create_connection(lambda:TCPEchoClientProtocol(message,loop),host='127.0.0.1',port=8888)
    transport,protocol=loop.run_until_complete(coro)#如果建立连接失败，则抛出异常
    loop.run_forever()
    loop.close()
