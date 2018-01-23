import asyncio
async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result("Future is done")#表示这个future已经执行完成
    return future.result

if __name__=="__main__":
    loop=asyncio.get_event_loop()
    future=asyncio.Future()
    asyncio.ensure_future(slow_operation(future))
    #如果传入的是future对象，那么直接返回，因为Task 对象是future对象的子类
    #如果传入的是coroutine函数，那么包装成Task对象 放入事件队列，等到合适时机执行 ，
    # Task是执行coroutine的载体 Task是coroutine向外部展示的形态
    #先执行内部的future
    loop.run_until_complete(future)
    #The run_until_complete() method uses internally the add_done_callback() method to be notified when the future is done.
    print(future.result())
    loop.close()
