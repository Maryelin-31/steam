# -*- coding: utf-8 -*-


from zml import *


def get_perm(seepage, face_ids):
    """
    返回平均的渗透率
    """
    assert isinstance(seepage, Seepage)
    assert len(face_ids) > 0
    sum = 0
    for face_id in face_ids:
        assert face_id < seepage.face_number, f'face_id = {face_id} while seepage.face_number = {seepage.face_number}'
        face = seepage.get_face(face_id)
        assert isinstance(face, Seepage.Face)
        sum += face.get_attr(4)
    return sum / len(face_ids)
