# -*- coding: utf-8 -*-


from zmlx import *
from zmlx.data.lyy_discs import get_discs


def get_box():
    """
    返回数据的范围
    """
    return -7.5, -5, -7.5, 7.5, 5, 7.5


def create_lat():
    """
    创建格子，并将基于这个格子来创建流动的网格
    模型的大小：
        x: 15
        y: 10
        z: 15
    """
    return Lattice(box=get_box(), shape=(15 / 60, 10 / 5, 15 / 60))


def create_seepage_mesh(lat=None):
    """
    创建一个用于计算的矩形网格
    """
    if lat is None:
        lat = create_lat()
    mesh3 = Mesh3.create_cube(lat=lat)
    return SeepageMesh.from_mesh3(mesh3=mesh3)


def create_discs(lat=None, da_set=None, seepage_mesh=None):
    """
    返回在这个体系内可以使用的圆盘数据。 这里已经确定了Disc和Cell的关系
    """
    if lat is None:
        lat = create_lat()
    if seepage_mesh is None:
        seepage_mesh = create_seepage_mesh(lat=lat)

    dist = max(*[abs(x) for x in lat.box])  # 最远的距离
    lyy_discs = get_discs(da_set=da_set)
    result = Disc3Vec()
    for i in range(len(lyy_discs)):
        disc = Disc3.get_copy(lyy_discs[i])
        disc.add_scale(max(1, dist / 7.5))
        disc.get_lat_inds(lat=lat, buffer=disc.cell_ids)
        seepage_mesh.find_inner_face_ids(cell_ids=disc.cell_ids, buffer=disc.face_ids)
        if len(disc.face_ids) > 10:
            result.append(disc)
    print(f'Disc count = {len(result)} / {len(lyy_discs)}')
    return result


if __name__ == '__main__':
    print(create_discs())
