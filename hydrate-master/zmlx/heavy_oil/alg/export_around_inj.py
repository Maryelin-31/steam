# -*- coding: utf-8 -*-


from zmlx import *
import get_cell_attr
# from heavy_oil.alg.get_cell_attr import get_temperature
from zmlx.alg.get_cells_around_seg import get_cell_ids_around_seg


def export_around_inj():
    folder = os.path.join('data', 'seepage')
    print(folder)
    cell_ids = None
    data = []
    for name in os.listdir(folder):
        l = len('00000000003650_79324')
        t = float(name[0:l].replace('_', '.')) / 365.0
        fpath = os.path.join(folder, name)
        print(f't = {t}, fpath = {fpath}')
        seepage = Seepage(fpath=fpath)
        if cell_ids is None:
            cell_ids = []
            for x in (-3.75, 3.75):
                for z in (-4, 4):
                    seg = (x, -5, z), (x, 5, z)
                    dist = 1.5
                    cell_ids = cell_ids + get_cell_ids_around_seg(seg=seg, dist=dist, model=seepage)
            with open('cell_pos.txt', 'w') as file:
                for cell_id in cell_ids:
                    cell = seepage.get_cell(cell_id)
                    x, y, z = cell.pos
                    file.write(f'{x}  {y}  {z} \n')
        data.append([t,
                     get_temperature(seepage, cell_ids),
                     get_kerogen_mass(seepage, cell_ids),
                     get_heavy_oil_mass(seepage, cell_ids),
                     get_light_oil_mass(seepage, cell_ids),
                     get_water_mass(seepage, cell_ids),
                     get_gas_mass(seepage, cell_ids)])
    np.savetxt('mass_temp_vs_time_around_heat_inj.txt', np.array(data))
    print('Succeed!')


