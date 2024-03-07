import os

# 是否开发模式。
def is_debug_mode():
    '''
    一般Python项目，通过`Run/Debug Configurations`配置，
    可设置启动参数`Parameters`，如`--debug`开启开发模式，通过命令行运行时也可以添加`--debug`来开启
    但Django的`Run/Debug Configurations`中
    只能修改环境变量，添加`DEBUG=1`开启
    而通过命令行直接运行，没有设置`DEBUG`环境变量，所以值会是`False`
    '''
    # 检查命令行参数`--debug`是否存在
    for arg in os.sys.argv:
        if arg == '--debug':
            return True

    # 检查环境变量`DEBUG`是否为`1`
    if os.environ.get("DEBUG") == '1':
        return True
    return False


def is_local_mode():
    '''
    判断是否本地模式。是因为本地连接的数据库和线上的不一样，诸如类似区别，所以需要判断
    参考`is_debug_mode`
    '''
    for arg in os.sys.argv:
        if arg == '--local':
            return True
    if os.environ.get("LOCAL") == '1':
        return True
    return False


def dev_dis(dev, dis):
    '''
    获取和开发模式相关的变量
    如果是开发模式，返回开发环境下的配置
    否则返回生产环境下的配置
    '''
    return dev if is_debug_mode() else dis

def loc_srv(loc, srv):
    '''
    参考`dev_dis`
    '''
    return loc if is_local_mode() else srv

if __name__ == '__main__':
    print(is_debug_mode())
    print(is_local_mode())
    print(dev_dis('dev', 'dis'))
    print(loc_srv('loc', 'srv'))
