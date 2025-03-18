# -*- coding: utf-8 -*-


from zml import *


def get_mass(seepage, cell_ids, fluid_id):
    """
    返回给定Cell内给定ID的流体的质量的总和
    """
    assert isinstance(seepage, Seepage)
    mass = 0
    for cell_id in cell_ids:
        assert cell_id < seepage.cell_number, f'cell_id = {cell_id} while seepage.cell_number = {seepage.cell_number}'
        cell = seepage.get_cell(cell_id)
        assert isinstance(cell, Seepage.Cell)
        if is_array(fluid_id):
            flu = cell.get_fluid(fluid_id[0])
            for i in range(1, len(fluid_id)):
                flu = flu.get_component(fluid_id[i])
        else:
            flu = cell.get_fluid(fluid_id)
        mass += flu.mass
    return mass


def get_kerogen_mass(seepage, cell_ids):
    """
    返回所有Cell中<干酪根>的总的质量
    """
    return get_mass(seepage, cell_ids, [4, 0])


def get_char_mass(seepage, cell_ids):
    """
    返回所有Cell中<char>的总的质量
    """
    return get_mass(seepage, cell_ids, [4, 1])


def get_heavy_oil_mass(seepage, cell_ids):
    """
    返回所有Cell中<重油>的总的质量
    """
    return get_mass(seepage, cell_ids, 3)


def get_light_oil_mass(seepage, cell_ids):
    """
    返回所有Cell中<轻油>的总的质量
    """
    return get_mass(seepage, cell_ids, 2)


def get_water_mass(seepage, cell_ids):
    """
    返回所有Cell中<水>的总的质量
    """
    return get_mass(seepage, cell_ids, 1)


def get_gas_mass(seepage, cell_ids):
    """
    返回所有Cell中<甲烷气体>的总的质量
    """
    return get_mass(seepage, cell_ids, [0, 0])


def get_steam_mass(seepage, cell_ids):
    """
    返回所有Cell中<蒸汽>的总的质量
    """
    return get_mass(seepage, cell_ids, [0, 1])

