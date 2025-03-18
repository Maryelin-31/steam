# -*- coding: utf-8 -*-


from zml import *
from zmlx.heavy_oil.alg.get_opened_outcrop import get_opened_outcrop
import os


def export_opened_outcrop(odir, idir):
    if not os.path.isdir(idir):
        return
    names = os.listdir(idir)
    if len(names) == 0:
        return
    disc0 = Disc3Vec(path=os.path.join(idir, names[0]))
    for name in names:
        ipath = os.path.join(idir, name)
        print(f'Processing {ipath} -> ', end=None)
        disc1 = Disc3Vec(path=ipath)
        outcrop = get_opened_outcrop(disc1, disc0)
        opath = make_parent(os.path.join(odir, name))
        np.savetxt(opath, outcrop)
        print(f'{opath}. Succeed!')

