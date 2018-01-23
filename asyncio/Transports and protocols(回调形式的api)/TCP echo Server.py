import asyncio
class TCPEchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print(transport)
        self.peername=transport.get_extra_info('peername')
        print('Connection from {}'.format(self.peername))
        self.transport=transport
    def data_received(self, data):
        message=data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        #print('Close the client socket')
        #self.transport.close()
    def connection_lost(self, exc):
        print("The connection from {} is closed".format(self.peername))
        '''
        Transport.close() can be called immediately after WriteTransport.write() even if data are not sent yet on the socket: both methods are asynchronous. 
        yield from is not needed because these transport methods are not coroutines
        To have a reliable execution order, use stream objects in a coroutine with yield from. For example, the StreamWriter.drain() coroutine can be used to wait until the write buffer is flushed.

        全异步，关闭之前可能发送不完
        如果想用协程，就用Stream 类
        '''
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    # 端口多路复用
    #服务端每个连接一个接收通道（transport)
    coro = loop.create_server(TCPEchoServerProtocol, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)#成功搭建起来一个TCP服务器
    print(server)#server对象中有一个sockets 属性 是一个list list里面每个元素是一个socket对象
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())#等待server.close()结束
    loop.close()
