import asyncio
async def tcp_echo_client(message,loop):
    reader,writer=await asyncio.open_connection(host='127.0.0.1',port=8888,loop=loop)
    print('Send: %r' % message)
    writer.write(message.encode())
    await writer.drain()#将缓冲区的数据都发送出去 （刷新缓冲区）
    data=await reader.read(n=100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()
if __name__=='__main__':
    message = 'Hello World!'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(message, loop))
    loop.close()

