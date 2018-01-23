import socket
from selectors import DefaultSelector ,EVENT_READ,EVENT_WRITE,_fileobj_to_fd
#EVENT_READ 1 EVENT_WRITE 2
selector=DefaultSelector()
stopped=False
urls_todo={'/','/1','/2','/3','/4','/5','/6','/7','/8','/9'}
class Crawler(object):
    def __init__(self,url):
        self.url=url
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.response=b''
    def fetch(self):
        try:
            self.sock.connect((socket.gethostbyname('example.com'),80))
        except BlockingIOError:
            pass
        selector.register(fileobj=_fileobj_to_fd(self.sock),events=EVENT_WRITE,data=self.connected)#返回的是event_key
    def connected(self,key):
        selector.unregister(fileobj=key.fd)#登记之前先要登出
        print("key:",key)
        get_request='GET {} HTTP/1.0\r\nHost:example.com\r\n\r\n'.format(self.url)
        self.sock.send(get_request.encode())
        selector.register(key.fd,EVENT_READ,self.read_response)
    def read_response(self,key):
        print("key:", key)
        global stopped
        chunk=self.sock.recv(4096)
        if chunk:
            self.response+=chunk
        else:#无消息可读了，就登出 读事件
            print("response:" ,self.response.decode(encoding='utf-8',errors='ignore'))
            selector.unregister(key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped=True
def loop():
    while not stopped:
        event=selector.select()
        #阻塞， 直到一个事件发生
        for event_key,event_mask in event:
            callback=event_key.data
            callback(event_key)
if __name__=='__main__':
    print(type(urls_todo))
    import time
    start=time.time()#floating point number
    for url in urls_todo:
        crawler=Crawler(url)
        crawler.fetch()
    loop()
    print(time.time()-start)





