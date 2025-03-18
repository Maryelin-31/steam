

# from heavy_oil.chang7.create_interp import create_interp
from create_interp import create_interp
import numpy as np
from zmlx.alg.clamp import clamp


"""
原来的单位是立方米每吨（假设为1），则考虑上气体的密度为0.7，岩石的密度为2.5，则每立方米的岩石，含有的气体的质量为2.5*0.5=1.75kg
考虑到埋深约为1500米，原始地层压力取20Mpa，温度约100度，此时甲烷的密度约为150，所以，如果按照体积来算的，1立方岩石中原始的
状态下，含有的气体的体积约为1.75/150=0.0117立方的游离气。

原始数据的最大值为2，徐涛取值为1，这里需要乘以2倍，然后再乘以0.0117，就可以得到不同深度下，每立方岩石中含有的气体的体积
"""
gas = create_interp('Free gas content.txt', 0.0117*2.0)


"""
原图中的含水量，我们不妨认为就是每立方储层中含有的水的体积，所以不需要调整
"""
wat = create_interp('water saturation.txt')


"""
轻质油。原来的单位是mg/g（等于千克/吨），考虑岩石的密度是2.5，乘以2.5后，就得到千克/方，再除以密度（假设为1000），就得到了立方米/方，就是
体积的比例
"""
light_oil = create_interp('Retained light oil volume.txt', 2.5/1000.0)


"""
简化起见，重质油采用了轻质一样的计算方法，则
"""
all_oil = create_interp('Amount of retained light + medium + heavy oil.txt', 2.5/1000.0)

"""
干酪根. 和前面油的计算方法一样，不过这里把密度取为1500
"""
kerog = create_interp('residual oil potential.txt', 2.5/1500.0)

"permability create 10.1144/petgeo2016-146"
perm = create_interp('permeability.txt')

por = create_interp('porosity.txt')
"""
深度从1570到1600，取30米. 最后数据：

0: coordenada z
1: Porosidad
2: saturación de gas
3: saturación de agua
4: Saturación de petróleo ligero
5: Saturación de petróleo pesado
6: saturación de kerógeno
7:perm
"""
data = np.zeros(shape=(100, 9))
data[:, 0] = np.linspace(1818, 1843, 100)


for i in range(data.shape[0]):
    z = data[i, 0]
    fai = clamp(gas(z) + wat(z) + all_oil(z) + kerog(z), 0.001, 1)
    data[i, 1] = fai
    # 各个饱和度
    data[i, 2] = gas(z) / fai
    data[i, 3] = wat(z) / fai
    ao = all_oil(z)
    lo = min(light_oil(z), ao)
    data[i, 4] = lo / fai
    data[i, 5] = (ao - lo) / fai
    data[i, 6] = kerog(z) / fai
    data[i, 7] = perm(z) / fai
    data[i, 8] = por(z) / fai
    
np.savetxt('data.txt', data)


