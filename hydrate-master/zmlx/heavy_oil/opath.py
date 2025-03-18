# -*- coding: utf-8 -*-


from zmlx.alg.opath import opath as get_opath


# 文件夹名称
folder = 'HeavyOil'


def opath(*args):
    """
    返回数据目录
    """
    return get_opath(folder, *args)


if __name__ == '__main__':
    print(opath())
    print(opath('x'))

