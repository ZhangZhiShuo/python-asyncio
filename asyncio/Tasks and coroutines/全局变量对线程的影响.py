import asyncio
import threading
import time
#线程拥有一个资源块，可共用全局变量
#每个进程拥有自己的资源块，需要进程间的通信
#run_forever之前就要将loop.stop()添加到回调中
loop=asyncio.get_event_loop()
test_list=[1,2]
async def stop_loop():
    print("The loop will be stopped")
    loop.stop()
    print("The loop stopped succeed")
async def my_coro():
    await asyncio.sleep(1)
    return "Hello to you"
class My_Future_Thread(threading.Thread):
    def __init__(self):
        super(My_Future_Thread,self).__init__()
    def run(self):
        #time.sleep(1)
        test_list.append(3)
        coro=my_coro()
        future = asyncio.run_coroutine_threadsafe(coro=coro, loop=loop)
        '''
            Submit a  coroutine object  to a given event loop.

          Return a   concurrent.futures.Future   to access the result.


            '''
        # assert future.result(timeout=1)==3
        try:
            # future.cancel()
            result = future.result(timeout=None)  # 在这个方法前调用cancel 方法会触发 CancelledError

            '''
            result(timeout=None) 
    Return the value returned by the call. If the call hasn’t yet completed then this method will wait up to timeout seconds. 
    If the call hasn’t completed in timeout seconds, then a  concurrent.futures.TimeoutError  will be raised. timeout can be an int or float. 
    If timeout is not specified or None, there is no limit to the wait time.

    If the future is cancelled before completing then CancelledError will be raised.

    If the call raised, this method will raise the same exception.


            '''
        except asyncio.TimeoutError:
            print('The coroutine took too long, cancelling the task...')
            future.cancel()
        except asyncio.CancelledError:
            print('the future is cancelled before completing')
        except Exception as exc:
            print('The coroutine raised an exception: {!r}'.format(exc))
        else:
            print('The coroutine returned: {!r}'.format(result))
        finally:
            print("test_list in child_thread:" ,test_list)
            callback=stop_loop()
            asyncio.run_coroutine_threadsafe(coro=callback,loop=loop)#可由其他线程向run loop 的线程添加所要执行的coroutine
            #loop.call_soon(callback=loop.stop)#调用范围和run loop 的线程一致




if __name__=='__main__':
    t=My_Future_Thread()
    t.start()
    test_list.append(4)
    print("test_list in main_thread",test_list)
    loop.run_forever()
    loop.close()
    print("The loop closed succeed")








