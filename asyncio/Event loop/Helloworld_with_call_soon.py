import asyncio
import functools
def hello_world(loop):
    print("Hello world")
    #loop.stop()#停止履带的转动，但是并不销毁履带，履带上的任务还会保留，下一次调用run的时候履带上的任务继续按次序被执行工人所执行
if __name__=='__main__':
    loop=asyncio.get_event_loop()
    loop.call_soon(functools.partial(hello_world,loop=loop))#as soon as possible 立即执行
    loop.run_forever()#需要由loop.stop()来停止履带 它才会运行下一条语句
    loop.close()#销毁传输的履带和辞退执行工人，这个工作是不可逆转的