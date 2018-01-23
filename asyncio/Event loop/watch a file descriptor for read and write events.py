import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair
import functools
import time
def reader(rsock,loop):
    data=rsock.recv(100)
    print("Received:",data.decode())
    loop.remove_reader(rsock)
    loop.stop()
def writer():
    print("Writing......")
    time.sleep(2)
def writing(wsock):
    wsock.send("Hello to you ".encode())
def close_all(loop,rsock,wsock):
    loop.close()
    wsock.close()
    rsock.close()

if __name__=="__main__":
    rsock,wsock=socketpair()#返回一对连接的套接字对象
    loop=asyncio.get_event_loop()
    loop.add_reader(fd=rsock,callback=functools.partial(reader,rsock=rsock,loop=loop))#当fd对象读入性可用时调用callback函数
    #loop.add_writer(fd=wsock,callback=writer)#当fd对象的写入性可用时调用callback函数
    loop.call_soon(callback=functools.partial(writing,wsock=wsock))
    loop.run_forever()
    close_all(loop,rsock,wsock)
