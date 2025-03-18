# -*- coding: utf-8 -*-


from zmlx.heavy_oil.chang7 import *

from zmlx.alg.clamp import clamp


def create_initial():
    """
    创建初始场
    """

    def get_initial_t(x, y, z):
        """
        the initial temperature
        """
        return 338.0 + 22.15 - 0.0443 * z

    def get_initial_p(x, y, z):
        """
        the initial pressure
        """
        return 20.0e6 - 1e4 * z

    def get_perm(x, y, z):
        """
        the initial permeability
            这里，基质的渗透率也没有必要做成是孔隙度相关了，因为后续的导流能力，主要还是由裂缝产生的
        """
        return 1.0e-17

    def get_initial_s(x, y, z):
        """
        the initial saturation ([ch4, Vapor], water, light_oil, heavy_oil, [kerogen, char])
        """
        sg = z2sg(z)
        assert sg >= 0, f'sg = {sg}'

        sw = z2sw(z)
        assert sw >= 0

        slo = z2slo(z)
        assert slo >= 0, f'slo = {slo}'

        sho = z2sho(z)
        assert sho >= 0, f'sho = {sho}'

        sk = clamp(z2sk(z), 0, 0.7)  # 对最大值进行必要的限制，确保不是纯的固体
        assert sk >= 0

        return (sg, 0.0), sw, slo, sho, (sk, 0)

    def get_fai(x, y, z):
        """
        porosity
        """
        return z2porosity(z)

    def get_denc(x, y, z):
        """
        porosity
        """
        return 2500 * 2000

    def get_heat_cond(x, y, z):
        return 2.0

    return {'porosity': get_fai, 'pore_modulus': 100e6, 'p': get_initial_p,
            'temperature': get_initial_t,
            'denc': get_denc, 's': get_initial_s,
            'perm': get_perm, 'heat_cond': get_heat_cond, 'sample_dist': 0.01, 'dist': 0.1}


if __name__ == '__main__':
    print(create_initial())
