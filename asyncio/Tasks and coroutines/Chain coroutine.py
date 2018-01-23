import asyncio
async def add(x,y):
    print("Add %d + %d" %(x,y))
    await asyncio.sleep(1)
    return x+y
async def print_sum(x,y):
    result=await add(x,y)#等待add协程执行完，获取他的return的结果
    print("%d+%d=%d"%(x,y,result))
if __name__=="__main__":
    loop=asyncio.get_event_loop()
    loop.run_until_complete(print_sum(1,2))