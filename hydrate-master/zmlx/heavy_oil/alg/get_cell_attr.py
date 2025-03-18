# -*- coding: utf-8 -*-


from zml import *


def get_cell_attr(seepage, cell_ids, attr_id):
    """
    返回给定Cell内给定ID的流体的质量的总和
    """
    assert isinstance(seepage, Seepage)
    assert len(cell_ids) > 0
    sum = 0
    for cell_id in cell_ids:
        
        assert cell_id < seepage.cell_number, f'cell_id = {cell_id} while seepage.cell_number = {seepage.cell_number}'
        cell = seepage.get_cell(cell_id)
        assert isinstance(cell, Seepage.Cell)
        sum += cell.get_attr(attr_id)
    return sum / len(cell_ids)


def get_temperature(seepage, cell_ids):
    return get_cell_attr(seepage, cell_ids, 1)


def get_pressure(seepage, cell_ids):
    return get_cell_attr(seepage, cell_ids, 3)


