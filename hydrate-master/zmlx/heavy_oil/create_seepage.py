# -*- coding: utf-8 -*-


from zmlx import *
from zmlx.heavy_oil.initial import *
from zmlx.alg.linspace import linspace
from zmlx.utility.HeatInjector import HeatInjector
from zmlx.kr.create_krf import create_krf


def create_seepage(space, power, srg=0.05, srw=0.05, sro=0.05):
    """
    创建模型
    """
    # 创建网格并进而创建模型
    assert space.config is not None
    ini = create_initial()
    space.seepage = space.config.create(space.seepage_mesh, **ini)
    space.seepage.set(gravity=(0, 0, -10))

    # 相对渗透率
    space.seepage.set_kr(space.config.igas, *create_krf(srg, 3.0))
    space.seepage.set_kr(space.config.iwat, *create_krf(srw, 3.0))
    space.seepage.set_kr(space.config.ilight_oil, *create_krf(sro, 3.0))
    space.seepage.set_kr(space.config.iheavy_oil, *create_krf(sro, 3.0))

    # 时间步长策略
    space.config.set_dv_relative(space.seepage, 0.5)  # 每一个时间步流过的距离与网格大小的比值
    space.config.set_dt(space.seepage, 0.01)  # 时间步长的初始值
    space.config.set_dt_max(space.seepage, 24 * 3600 * 7)  # 时间步长的最大值 <一周>
    space.config.set_dt_min(space.seepage, 3600)  # 最小步长1小时

    # 添加虚拟Cell用于生产(注：虚拟Cell内务必为气水共存的状态!)
    pos = (-7.5, 1e6, 0)  # 添加虚拟Cell，虚拟Cell位于<非常远>的位置
    virtual_cell = space.config.add_cell(space.seepage, pos=pos, porosity=1.0e3, pore_modulus=100e6,
                                         temperature=ini['temperature'](*pos), p=3e6,
                                         s=((0, 0), 1, 0, 0, (0, 0)))

    y0, y1 = space.seepage_mesh.get_pos_range(1)
    print(f'y0 = {y0}, y1 = {y1}')

    cell_ids = set()
    for y in linspace(y0, y1, 100):
        cell = space.seepage.get_nearest_cell(pos=(-7.5, y, 0))
        cell_ids.add(cell.index)
    for cell_id in cell_ids:
        space.config.add_face(space.seepage, virtual_cell, space.seepage.get_cell(cell_id),
                              heat_cond=0, perm=1e-14,
                              area=1.0,
                              length=1.0,
                              )  # todo: 要检查这里的连接强度是否合适

    # 创建压力控制
    space.prectrl = PressureController(virtual_cell, t=[0, 1e10], p=[3e6, 3e6])

    # 添加一个单元的监视，以输出生产曲线(注意：这里传递给monitor的时间的单位为天)
    # 必须将prectrl一起监控
    space.monitor = SeepageCellMonitor(get_t=lambda: space.config.get_time(space.seepage),
                                       cell=(virtual_cell, space.prectrl))

    # 控制底部和顶部的温度
    space.heat_injectors = []
    if True:
        z0, z1 = space.seepage_mesh.get_pos_range(2)
        t0 = ini['temperature'](0, 0, z0)
        t1 = ini['temperature'](0, 0, z1)
        n0 = 0
        n1 = 0
        area = (15 / 60) * (20 / 6)
        for cell_id in range(space.seepage_mesh.cell_number):
            z = space.seepage_mesh.get_cell(cell_id).pos[2]
            if abs(z - z0) < 1.0e-6:
                space.heat_injectors.append(HeatInjector(cell=space.seepage.get_cell(cell_id),
                                                         ca_mc=space.config.cell_keys['mc'],
                                                         ca_t=space.config.cell_keys['temperature'],
                                                         temp=t0,
                                                         cond=area / 10.0,  # 一个厚度为10m的缓冲层
                                                         ))
                n0 += 1
            if abs(z - z1) < 1.0e-6:
                space.heat_injectors.append(HeatInjector(cell=space.seepage.get_cell(cell_id),
                                                         ca_mc=space.config.cell_keys['mc'],
                                                         ca_t=space.config.cell_keys['temperature'],
                                                         temp=t1,
                                                         cond=area / 10.0,  # 一个厚度为10m的缓冲层
                                                         ))
                n1 += 1
        print(f'Count of Thermal boundary Cell: {n0}, {n1}')

    # 用于注热的Cell
    cell_ids = set()
    for x in (-3.75, 3.75):
        for z in (-4, 4):
            for y in linspace(y0, y1, 100):
                cell = space.seepage.get_nearest_cell(pos=(x, y, z))
                cell_ids.add(cell.index)

    print(f'count of cells for heat injection: {len(cell_ids)}')
    assert len(cell_ids) > 0

    power /= len(cell_ids)
    for cell_id in cell_ids:
        cell = space.seepage.get_cell(cell_id)
        print(f'heatinj. pos = {cell.pos}')
        space.heat_injectors.append(HeatInjector(cell=cell, power=power, ca_mc=space.config.cell_keys['mc'],
                                                 ca_t=space.config.cell_keys['temperature']))
