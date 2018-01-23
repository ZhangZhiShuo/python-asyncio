import asyncio
import datetime
async def display_date(loop):
    end_time=loop.time()+5.0
    while True:
        print("now:",datetime.datetime.now())
        if(loop.time()+1.0>=end_time):
            return "This is the result...."
            break;
        await asyncio.sleep(1)
        #event loop 中插入一个sleep 的coroutine the sleep coroutine creates an internal future which uses AbstractEventLoop.call_later() to wake up（唤醒） the task in 1 second.

def hello_world():
    print("Hello world!")
if __name__=="__main__":
    loop=asyncio.get_event_loop()
    loop.call_later(1.5, callback=hello_world)#先插入到事件队列中
    print(loop.run_until_complete(display_date(loop)))

    loop.close()