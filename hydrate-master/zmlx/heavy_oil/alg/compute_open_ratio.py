# -*- coding: utf-8 -*-


from zml import *


def compute_open_ratio(disc1, disc0, attr_id):
    """
    计算disc1中各个圆盘张开的比例，并存储到attr_id定义的属性内
    """
    assert isinstance(disc1, Disc3Vec)
    assert isinstance(disc0, Disc3Vec)
    assert len(disc1) == len(disc0), f'The number of disc should be equal'

    for i in range(len(disc1)):
        n0 = disc0[i].face_ids.size
        n1 = disc1[i].face_ids.size
        assert n0 >= n1
        if n0 > 0:
            disc1[i].set_attr(attr_id, (n0 - n1) / n0)
        else:
            disc1[i].set_attr(attr_id, 0)

    return disc1


