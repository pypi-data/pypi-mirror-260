'''
输出方法执行的日志以及消耗时间
'''
import time, functools, inspect


default_printer = print # 全局默认的输出方法
default_starter = '开始'
default_starter_ch = '>>>'
default_ender = '结束'
default_ender_ch = '<<<'
default_cost_ch = '耗时'
default_time_ch = '秒'
default_stack_level = 3


def func_time(func_desc=None, printer=None):
    def decorator(func):
        desc = func_desc if func_desc else func.__name__
        prtr = printer if printer else default_printer # 如果不提供输出方法，使用默认的输出方法
        prtr = prtr if prtr else print # 如果默认的输出方法也没有，使用print方法
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            kw = {}
            try:
                if bool(inspect.signature(prtr).parameters.get('kwargs')) or bool(inspect.signature(prtr).parameters.get('stacklevel')):
                    kw['stacklevel'] = default_stack_level # 针对`alog.Logger`参数，适配调用堆栈层级，输出方法真正调用点的信息
            except:
                pass
            prtr(f'{desc}{default_starter} {default_starter_ch}', **kw)
            __start__ = time.time()
            result = func(*args, **kwargs)
            __end__ = time.time()
            prtr(f'{desc}{default_ender} {default_ender_ch} {default_cost_ch}: {__end__ - __start__:.1f}{default_time_ch}', **kw)
            return result
        return wrapper
    return decorator


def test():
    @func_time('某个方法', print)
    def some_func(n):
        time.sleep(n)

    some_func(1)


if __name__ == '__main__':
    test()
    pass
