# -*- coding: utf-8 -*-


from zml import *
from zmlx.heavy_oil.alg.get_perm import get_perm
from zmlx.heavy_oil.mesh import create_seepage_mesh
from zmlx.alg.get_faces_around_seg import get_face_ids_around_seg


def export_perm_vs_time(output_file, folder):
    """
    读取folder中的文件，并且提取渗透率随着时间的变化
    """
    seepage_mesh = create_seepage_mesh()
    x = -7.5
    z = 0
    face_ids1 = get_face_ids_around_seg(seg=((x, -5, z), (x, 5, z)), dist=1.5, model=seepage_mesh)
    face_ids2 = get_face_ids_around_seg(seg=((x, -5, z), (x, 5, z)), dist=3.0, model=seepage_mesh)
    face_ids3 = range(seepage_mesh.face_number)

    data = []
    for name in os.listdir(folder):
        l = len('00000000003650_79324')
        t = float(name[0:l].replace('_', '.')) / 365.0
        fpath = os.path.join(folder, name)
        print(f't = {t}, fpath = {fpath}')
        seepage = Seepage(fpath=fpath)
        data.append([t,
                     get_perm(seepage, face_ids1),
                     get_perm(seepage, face_ids2),
                     get_perm(seepage, face_ids3),
                     ])
    np.savetxt(output_file, np.array(data))
    print('Succeed!')
