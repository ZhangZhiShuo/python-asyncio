import asyncio

class UDPEchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print(transport)
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        #print("Close the socket")
        #self.transport.close() #OK

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        self.loop.stop()
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    message = "Hello World!"
    connect = loop.create_datagram_endpoint(
             lambda: UDPEchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 9999))
    transport, protocol = loop.run_until_complete(connect)
    print(transport)
    loop.run_forever()
    loop.close()
