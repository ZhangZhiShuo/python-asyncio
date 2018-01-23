import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        print("%s begin sleeping......." % name)
        await asyncio.sleep(1)
        #这个协程等待sleep 协程执行完才能执行 （await的功能 ）
        # sleep 协程 暂停自己,只是timeout之后调用call_later中注册的回调唤醒自己（yield from) 执行完毕
        print("%s stop sleeping......." % name)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))
if __name__=="__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
  loop.close()
