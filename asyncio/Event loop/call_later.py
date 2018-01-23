import asyncio
import datetime
import functools
def display_date(end_time,loop):
    print("datetime.now:",datetime.datetime.now())
    print("loop.time:",loop.time())
    if(loop.time()+1<end_time):
        loop.call_later(delay=1,callback=functools.partial(display_date,end_time=end_time,loop=loop))
    else:
        loop.stop()
if __name__=="__main__":
    loop=asyncio.get_event_loop()
    end_time=loop.time()+5
    loop.call_soon(callback=functools.partial(display_date,end_time=end_time,loop=loop))
    loop.run_forever()
    loop.close()