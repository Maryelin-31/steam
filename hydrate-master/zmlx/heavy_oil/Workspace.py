# -*- coding: utf-8 -*-


from zmlx.heavy_oil.mesh import *
from zmlx.heavy_oil.create_seepage import *
from zmlx.config import create_heavy_oil as create_config
from zmlx.heavy_oil.solve import solve
from random import uniform
import os


class Workspace:

    def __init__(self, power=0.0, srg=0.05, srw=0.05, sro=0.05, fperm=1.0e-15):
        """
        创建模型，并完成所有的初始化
        Create a model and complete all initializations
        """
        self.__create_seepage(power=power, srg=srg, srw=srw, sro=sro)
        self.__create_discs(fperm=fperm)

    def __create_seepage(self, power=0.0, srg=0.05, srw=0.05, sro=0.05):
        """
        step 1.
        创建渗流模型
        Create a seepage model
        """
        self.lat = create_lat()
        self.seepage_mesh = create_seepage_mesh(lat=self.lat)
        self.config = create_config()
        create_seepage(space=self, power=power, srg=srg, srw=srw, sro=sro)

    def __create_discs(self, fperm=1.0e-15):
        """
        step 2.
        根据格子，挑选那些在格子范围内能够使用的圆盘
        According to the grid, select those discs that can be 
        used within the range of the grid
        """
        assert isinstance(self.seepage, Seepage)
        self.da_set = 0
        self.da_k = 1
        self.da_pc = 2
        discs = create_discs(lat=self.lat, seepage_mesh=self.seepage_mesh, da_set=self.da_set)

        self.discs = Disc3Vec()
        for i in range(len(discs)):
            disc = discs[i]
            iset = round(disc.get_attr(self.da_set))
            assert iset in (0, 1, 2)
            if iset == 0:  # 水平的层理
                for face_id in disc.face_ids.to_list():
                    self.config.cond_updater.vk[face_id] += fperm
            else:
                disc.set_attr(self.da_k, fperm * 2)  # 裂缝的导流能力，设置为水平层理的2倍 The conductivity of the fracture is set to be twice that of the horizontal bedding
                disc.set_attr(self.da_pc, uniform(21e6, 100e6))  # 让这个强度在很大的范围内变化，从而模拟裂缝张开后在应力层面的相互影响 Let this intensity vary in a large range, thus simulating the interaction at the stress level after crack opening
                self.discs.append(disc)
        print(f'Count of disc: {len(self.discs)} / {len(discs)}')

    def solve(self, folder=None, time_max=3600 * 24 * 365 * 10,
              guimode=True, email=None, email_subject=None,
              close_after_done=True, save_dt=None):
        """
        执行求解过程
        Execute the solution process
        """

        def do_sol():
            if gui.exists():
                gui.title(f'Output: {folder}')
            solve(self, folder=folder, time_max=time_max, save_dt=save_dt)
            if email is not None:
                subject = f'HeavyOil_Solved' if email_subject is None else email_subject
                sendmail(email, subject=subject,
                         text=f'Working Folder: {folder}', name_from=None, name_to=None)

        if not guimode:
            do_sol()
        else:
            gui.execute(do_sol, close_after_done=close_after_done)

    @staticmethod
    def execute(power, folder, guimode, time_max, email, email_subject,
                close_after_done=True, srg=0.05, srw=0.05, sro=0.05, fperm=1.0e-15, save_dt=None):
        """
        利用给定的参数，执行建模和求解的所有的操作
        Perform all operations of modeling and solving 
        with the given parameters
        """
        space = Workspace(power=power, srg=srg, srw=srw, sro=sro, fperm=fperm)
        space.solve(folder=folder, time_max=time_max,
                    guimode=guimode,
                    email=email, email_subject=email_subject,
                    close_after_done=close_after_done, save_dt=save_dt)

    @staticmethod
    def execute_vari_power_perm(power=20000.0, fperm=1.0e-15, folder=None, save_dt=None):
        """
        用于将功率和渗透率作为变量，并计算一系列的算例
        """
        from heavy_oil.opath import opath
        if folder is None:
            folder = opath('VariPowerPerm', '%0.4e_%0.4e' % (power, fperm), 'data')
        assert not os.path.exists(folder), f'output folder exists: {folder}'
        Workspace.execute(power=power, fperm=fperm, folder=folder,
                          srg=0.05, srw=0.05, sro=0.05,
                          guimode=False,
                          time_max=3600 * 24 * 365 * 10,
                          email=None, email_subject=None,
                          close_after_done=True, save_dt=save_dt)


if __name__ == '__main__':
    space = Workspace()
