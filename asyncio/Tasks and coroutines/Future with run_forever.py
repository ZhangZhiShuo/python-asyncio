import asyncio
import functools
async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result("Future is done")#表示这个future已经执行完成
def got_result(future,loop):
    print(future.result())
    loop.stop()
if __name__=="__main__":
    loop1=asyncio.get_event_loop()
    future=asyncio.Future()
    asyncio.ensure_future(slow_operation(future=future))
    future.add_done_callback(functools.partial(got_result,loop=loop1))#future 对象谁调用的这个方法谁自动传入
    loop1.run_forever()
    loop1.close()