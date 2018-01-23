def yield_from_generator():
    yield from generator()
def generator():
    x=yield
    yield x+1
if __name__=='__main__':
    g=yield_from_generator()
    print(g)
    next(g)#start 生成器运行，暂停在第一个yield处
    retval=g.send(1)
    print(retval)
    #g.throw(StopIteration)
