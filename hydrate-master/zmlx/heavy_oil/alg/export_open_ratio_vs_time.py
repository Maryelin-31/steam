# -*- coding: utf-8 -*-


from zml import *
from zmlx.heavy_oil.alg.compute_open_ratio import compute_open_ratio
import os


def run():
    folder = os.path.join('data', 'discs')
    if not os.path.isdir(folder):
        return
    names = os.listdir(folder)
    if len(names) == 0:
        return
    disc0 = Disc3Vec(path=os.path.join(folder, names[0]))
    with open('time2open.txt', 'w') as file:
        for name in names:
            ipath = os.path.join(folder, name)
            print(f'Processing {ipath} -> ', end=None)
            disc1 = Disc3Vec(path=ipath)
            compute_open_ratio(disc1, disc0, 1)
            rr = 0
            for i in range(len(disc1)):
                rr += disc1[i].get_attr(1)
            rr /= len(disc1)
            l = len('00000000003650_79324')
            t = float(name[0:l].replace('_', '.')) / 365.0
            file.write(f'{t}  {rr}\n')
    print(f'Succeed!')

