import socket
from selectors import DefaultSelector ,EVENT_READ,EVENT_WRITE
selector = DefaultSelector()
stopped=False
urls_todo={'/','/1','/2','/3','/4','/5','/6','/7','/8','/9'}
class Future:
    def __init__(self):
        self.result=None
        self._callbacks=[]
    def add_done_callback(self,fn):
        self._callbacks.append(fn)
    def set_result(self,result):
        self.result=result
    def do_callback_list(self):
        for fn in self._callbacks:
            fn(self)
            self._callbacks.remove(fn)
    def __iter__(self):
        yield self
        return self.result
class Crawler:
    def __init__(self,url):
        self.url=url
        self.response=b''
    def fetch(self):
        sock=socket.socket()
        sock.setblocking(False)
        try:
            sock.connect((socket.gethostbyname('example.com'),80))
        except BlockingIOError:
            pass
        f=Future()
        def on_connected():
            f.set_result(None)
            f.do_callback_list()
        selector.register(sock.fileno(),EVENT_WRITE,on_connected)
        yield from f
        selector.unregister(sock.fileno())
        get_request = 'GET {} HTTP/1.0\r\nHost:example.com\r\n\r\n'.format(self.url)
        sock.send(get_request.encode())
        def on_readable():
            f.set_result(sock.recv(4096))
            f.do_callback_list()
        selector.register(sock.fileno(), EVENT_READ, on_readable)
        global stopped
        while True:

            chunk =yield from f #等号左边是接收的是send过来的值，等号右边是外部调用函数接收的值
            if chunk:
                self.response+=chunk
            else:
                print("response:", self.response.decode(encoding='utf-8', errors='ignore'))
                urls_todo.remove(self.url)
                selector.unregister(sock.fileno())
                if not urls_todo:
                      stopped=True
                break
class Task:
    def __init__(self,coro):
        self.coro=coro
        self.future=Future()
        self.future.set_result(None)
        self.next_step(self.future)#对象初始化便启动协程
        #单一职责，每种角色各司其职，如果还有工作没有角色来做，那就创建一个角色去做。没人来恢复这个生成器的执行么？没人来管理生成器的状态么？创建一个，就叫Task好了，很合适的名字。
    def next_step(self,future):#唤醒协程
        try:
            #send(None) next 唤醒协程 直到下次yield
            #下次yield 传出的值赋给next_future
            next_future=self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.next_step)
def loop():#事件捕获功能
    while not stopped:
         event=selector.select()
         for event_key,event_mask in event:
             callback=event_key.data
             callback()#调用回调函数
if __name__=='__main__':
    import time
    start =time.time()
    for url in urls_todo:
        crawler=Crawler(url)
        Task(coro=crawler.fetch())
    loop()
    print(time.time()-start)

