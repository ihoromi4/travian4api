import time
CALL_PERIOD = 0.5

def call_limiter(period):
    def decorator(func):
        def packer(self, *args, **kwargs):
            if hasattr(self, func.__name__ + '_last_call_time'):
                call_time = getattr(self, func.__name__ + '_last_call_time')
                if time.time() - call_time < period:
                    return getattr(self, func.__name__ + '_last_call_result')
            result = func(self, *args, **kwargs)
            setattr(self, func.__name__ + '_last_call_time', time.time())
            setattr(self, func.__name__ + '_last_call_result', result)
            return result
        packer.__name__ = func.__name__
        return packer
    return decorator

if __name__ == '__main__':
    class A:
        @call_limiter(1)
        def a(self):
            print('call a')
            return time.time()

    a = A()
    print(a.a)

    for i in range(9):
        print('result:', a.a())
        time.sleep(0.2)

