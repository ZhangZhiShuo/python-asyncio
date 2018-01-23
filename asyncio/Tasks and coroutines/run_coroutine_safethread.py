import asyncio
import threading
import time
async def my_coro():
    await asyncio.sleep(1)
    return "Hello to you"
async def stop_loop(loop):
    print("The loop will be stopped")
    loop.stop()
class My_Future_Thread(threading.Thread):
    def __init__(self,loop):
        super(My_Future_Thread,self).__init__()
        self.loop=loop
    def run(self):
        #coro = asyncio.sleep(delay=1, result=3)
        time.sleep(2)
        coro=my_coro()
        future = asyncio.run_coroutine_threadsafe(coro=coro, loop=self.loop)
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
            stop_loop_coro=stop_loop(loop=self.loop)
            asyncio.run_coroutine_threadsafe(coro=stop_loop_coro,loop=self.loop)
if __name__=='__main__':
    loop=asyncio.get_event_loop()
    t=My_Future_Thread(loop)
    t.start()
    loop.run_forever()

    loop.close()
    print("The loop closed succeed")








