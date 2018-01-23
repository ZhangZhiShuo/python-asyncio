import asyncio

class UDPEchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print(self.transport)
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)
        #self.transport.close() OK
    def connection_lost(self, exc):
        print("The connection is closed")
if __name__=='__main__':
   loop = asyncio.get_event_loop()
   print("Starting UDP server")
   # One protocol instance will be created to serve all client requests
   #服务端只有一个连接通道
   listen = loop.create_datagram_endpoint(
    UDPEchoServerProtocol, local_addr=('127.0.0.1', 9999))
   transport, protocol = loop.run_until_complete(listen)
   try:
      loop.run_forever()
   except KeyboardInterrupt:
      pass


   loop.close()
