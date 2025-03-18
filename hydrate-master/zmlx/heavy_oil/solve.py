# -*- coding: utf-8 -*-


from zmlx import *
from zmlx.alg import make_fname
import math


def plot_all(time, cells, faces, monitor, folder, config):
    """
    在界面上绘图。如果给定了folder，则在folder内创建figures文件夹，并在文件夹内保存绘图文件
    """
    if not gui.exists():
        # 如果不存在GUI界面，则没有执行此函数的必要(非GUI模式下，可能会有内存泄漏)
        return
    assert config is not None, 'The config not given when plot'

    kwargs = {'gui_only': False, 'title': f'plot when model.time={time2str(time)}'}
    x, y = [cell.pos[0] for cell in cells], [cell.pos[2] for cell in cells]

    # 绘制云图
    def get_path(name):
        if folder is not None:
            return os.path.join(folder, 'figures', name)

    def fig_name(key):
        return make_fname(time / (3600 * 24), folder=get_path(key), ext='.jpg', unit='d')

    tricontourf(x, y,
                [c.get_attr(config.cell_keys['pre']) for c in cells],
                caption='压力',
                fname=fig_name('pressure'), **kwargs)
    tricontourf(x, y,
                [c.get_attr(config.cell_keys['temperature']) for c in cells],
                caption='温度',
                fname=fig_name('temperature'),
                **kwargs)
    fa_t = config.flu_keys['temperature']
    tricontourf(x, y,
                [c.get_fluid(config.isol).get_component(0).get_attr(fa_t) for c in cells],
                caption='干酪根温度',
                fname=fig_name('kerogen_t'),
                **kwargs)
    tricontourf(x, y,
                [c.get_fluid(config.isol).get_component(0).mass for c in cells],
                caption='干酪根质量',
                fname=fig_name('kerogen_m'),
                **kwargs)
    tricontourf(x, y, [c.get_fluid(config.igas).vol_fraction for c in cells], caption='s_gas',
                fname=fig_name('s_gas'),
                **kwargs)
    tricontourf(x, y, [c.get_fluid(config.iwat).vol_fraction for c in cells], caption='s_wat',
                fname=fig_name('s_wat'),
                **kwargs)
    tricontourf(x, y, [c.get_fluid(config.ilight_oil).vol_fraction for c in cells], caption='s_light_oil',
                fname=fig_name('s_light_oil'),
                **kwargs)
    tricontourf(x, y, [c.get_fluid(config.iheavy_oil).vol_fraction for c in cells], caption='s_heavy_oil',
                fname=fig_name('s_heavy_oil'),
                **kwargs)
    tricontourf(x, y, [c.get_fluid(config.isol).vol_fraction for c in cells], caption='s_sol',
                fname=fig_name('s_sol'),
                **kwargs)

    x, y = [face.pos[0] for face in faces], [face.pos[2] for face in faces]
    tricontourf(x, y, [math.log10(f.get_attr(config.face_keys['perm'])) for f in faces], caption='perm',
                fname=fig_name('perm'),
                **kwargs)

    monitor.plot_prod(0,
                      fname=fig_name('gas_prod'),
                      **kwargs)
    monitor.plot_rate(0,
                      fname=fig_name('gas_rate'),
                      **kwargs)
    monitor.plot_prod(3,
                      fname=fig_name('oil_prod'),
                      **kwargs)
    monitor.plot_rate(3,
                      fname=fig_name('oil_rate'),
                      **kwargs)


def solve(space, folder, time_max, save_dt):
    """
    求解模型，并保存文件
    """
    assert isinstance(space.seepage, Seepage)
    assert isinstance(space.config, TherFlowConfig)

    if folder is not None:
        assert len(folder) > 0
        make_dirs(folder)
        print_tag(folder)

    y_min, y_max = space.seepage.get_pos_range(1)
    print(f'y_min = {y_min}, y_max = {y_max}')

    cells_for_plot = []
    for cell in space.seepage.cells:
        x, y, z = cell.pos
        if abs(y - y_min) < 0.1:
            cells_for_plot.append(cell)

    cell_ids = UintVector(value=[cell.index for cell in cells_for_plot])
    face_ids = space.seepage.find_inner_face_ids(cell_ids).to_list()
    faces_for_plot = []
    for face_id in face_ids:
        face = space.seepage.get_face(face_id)
        p0 = face.get_cell(0).pos
        p1 = face.get_cell(1).pos
        if abs(p0[2] - p1[2]) < 0.01:
            faces_for_plot.append(space.seepage.get_face(face_id))
    print(f'Count of face plot: {len(faces_for_plot)} / {len(face_ids)}')

    solver = ConjugateGradientSolver()
    solver.set_tolerance(1e-13)

    # 在迭代的过程绘图，此时仅仅绘图但不保存图片
    assert space.config is not None
    iterate = GuiIterator(space.config.iterate,
                          lambda: plot_all(time=space.config.get_time(space.seepage),
                                           cells=cells_for_plot,
                                           faces=faces_for_plot,
                                           monitor=space.monitor,
                                           folder=None,
                                           config=space.config,))

    def get_time():
        """
        获得保存文件的时候所使用的时间（用于生成文件名）
        """
        return space.config.get_time(space.seepage) / (3600 * 24)

    def get_save_dt(time):
        """
        返回数据保存的时间间隔
        """
        if save_dt is not None:
            return save_dt
        else:
            return min(30.0, max(2.0, time * 0.2))

    def print_cells(path):
        if path is None:
            return
        space.seepage.print_cells(path,
                                  properties=[lambda c: c.get_attr(space.config.cell_keys['temperature']), ])

    save_seepage = SaveManager(join_paths(folder, 'seepage'),
                               get_save_dt,
                               get_time, save=space.seepage.save, ext='.dat', time_unit='d')

    save_discs = SaveManager(join_paths(folder, 'discs'),
                             get_save_dt,
                             get_time, save=space.discs.save, ext='.dat', time_unit='d')

    save_cells = SaveManager(join_paths(folder, 'cells'),
                             get_save_dt,
                             get_time, save=print_cells, ext='.txt', time_unit='d')

    save_figs = SaveManager(None,
                            get_save_dt,
                            get_time,
                            save=lambda _: plot_all(time=space.config.get_time(space.seepage),
                                                    cells=cells_for_plot,
                                                    faces=faces_for_plot,
                                                    monitor=space.monitor,
                                                    folder=folder,
                                                    config=space.config,))

    save_prod = SaveManager(None,
                            get_save_dt,
                            get_time,
                            save=lambda _: space.monitor.save(join_paths(folder, 'prod.txt')))

    def save(**kwargs):
        save_seepage(**kwargs)
        save_discs(**kwargs)
        save_cells(**kwargs)
        save_figs(**kwargs)
        save_prod(**kwargs)

    while space.config.get_time(space.seepage) < time_max:
        years = space.config.get_time(space.seepage) / (3600 * 24 * 365)
        space.config.set_dv_relative(space.seepage, clamp(years / 5, 0.1, 0.8))
        space.prectrl.update(space.config.get_time(space.seepage))  # 确保边界压力
        if space.config.get_time(space.seepage) / (24 * 3600) > 10:
            iterate.ratio = 0.001
        else:
            iterate.ratio = 0.2

        # 注热热量
        dt = space.config.get_dt(space.seepage)
        for inj in space.heat_injectors:
            inj.work(dt)

        # 热流耦合的更新
        r = iterate(space.seepage, solver=solver)

        # 裂缝的张开 <修改渗透率>
        space.discs.modify_perm(space.config.cond_updater.vk, space.seepage,
                                space.config.cell_keys['pre'],
                                space.da_pc, space.da_k)

        """
        perm = space.seepage.get_attrs(key='faces',
                                       index=space.config.face_keys['perm']).to_numpy()
        print(f'Perm range. {np.min(perm)}, {np.max(perm)}')
        """

        # 更新g0，这样下一步就能用了
        space.config.cond_updater.update_vg0()

        # 数据监测
        space.monitor.update(dt=0.1)

        step = space.config.get_step(space.seepage)

        save()

        if step % 10 == 0:
            if gui.exists():
                print(
                    f'step = {step}, dt = {time2str(space.config.get_dt(space.seepage))}, '
                    f'time = {time2str(space.config.get_time(space.seepage))}, '
                    f'report={r}, krogen_mass={space.seepage.get_fluid_mass(fluid_id=(space.config.isol, 0))}')
            else:
                print(
                    f'{folder}: step = {step}, '
                    f'dt = {time2str(space.config.get_dt(space.seepage))}, '
                    f'time = {time2str(space.config.get_time(space.seepage))}, '
                    f'report={r}')

    # 保存最终的状态
    save(check_dt=False)
