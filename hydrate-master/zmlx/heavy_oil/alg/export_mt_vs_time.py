# -*- coding: utf-8 -*-


from zml import *
import os
from zmlx.heavy_oil.alg.get_cell_attr import get_temperature, get_pressure
from zmlx.heavy_oil.alg.get_cell_attr import *
# from zmlx.heavy_oil.alg.get_mass import *
from zmlx.heavy_oil.mesh import create_seepage_mesh
from zmlx.alg.get_cells_around_seg import get_cell_ids_around_seg


def export_mt_vs_time(output_file, folder, dist=1000):
    """
    读取folder中的文件，并且提取质量和温度信息
    """
    seepage_mesh = create_seepage_mesh()
    if dist > 100:
        # 默认，找到所有<正常的>Cell内的流体质量 <这里，取的是seepage_mesh的Cell数量，所以自然没有包含用于记录生产的虚拟Cell>
        cell_ids = range(seepage_mesh.cell_number)
    else:
        cell_ids = []
        for x in (-3.75, 3.75):
            for z in (-4, 4):
                seg = (x, -5, z), (x, 5, z)
                cell_ids = cell_ids + get_cell_ids_around_seg(seg=seg, dist=dist, model=seepage_mesh)
    print(cell_ids)

    data = []
    for name in os.listdir(folder):
        l = len('00000000003650_79324')
        t = float(name[0:l].replace('_', '.')) / 365.0
        fpath = os.path.join(folder, name)
        print(f't = {t}, fpath = {fpath}')
        seepage = Seepage()
        data.append([t,
                     get_temperature(seepage, cell_ids),
                     get_kerogen_mass(seepage, cell_ids),
                     get_heavy_oil_mass(seepage, cell_ids),
                     get_light_oil_mass(seepage, cell_ids),
                     get_water_mass(seepage, cell_ids),
                     get_gas_mass(seepage, cell_ids),
                     get_pressure(seepage, cell_ids),
                     get_steam_mass(seepage, cell_ids),
                     ])
    np.savetxt(output_file, np.array(data))
    print('Succeed!')
