# -*- coding: utf-8 -*-


from zml import *
from zmlx.heavy_oil.alg.compute_open_ratio import compute_open_ratio
from zmlx.alg.get_outcrop import get_outcrop


def get_opened_outcrop(disc1, disc0, box=None):
    """
    返回打开的露头数据
    """
    disc1 = compute_open_ratio(disc1, disc0, 2)
    if box is None:
        box = (-7.5, -5, -1000, 1000, 1000, 7.5)
    outcrop = get_outcrop(disc=disc1, box=box, attr_id=2)
    return np.array(outcrop)

