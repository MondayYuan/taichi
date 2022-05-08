from scene import Scene
import taichi as ti
from taichi.math import *
from math import sqrt

scene = Scene(voxel_edges=0.1, exposure=4) 
# 创建场景，指定体素描边宽度和曝光值
scene.set_floor(-1, (1.0, 1.0, 1.0)) 
# 地面高度
scene.set_background_color((0.5, 0.5, 0.4)) 
# 天空颜色
scene.set_directional_light((1, 1, -1), 0.2, (1, 1, 1)) 
# 光线方向和颜色

@ti.func
def create_sierpinski_carpet(pos, size, color_noise):
    for I in ti.grouped(ti.ndrange(size, size, size)):
        tmp = I.xyz
        new_size = size
        while new_size > 1:
            tmp_size = new_size // 3
            if tmp_size <= tmp.x < 2 * tmp_size and tmp_size <= tmp.y < 2 * tmp_size and tmp_size <= tmp.z < 2 * tmp_size:
                dis = max(abs(I.x - size//2), abs(I.y - size//2), abs(I.z - size//2))
                c = min(max(0, 1 - dis / (size // 2)), 1)
                scene.set_voxel(vec3(I.x+pos[0], I.y+pos[1], I.z+pos[2]), 1, vec3(c*0.8)+color_noise * ti.random())
                break
            else:
                new_size = tmp_size
                tmp %= new_size
        
@ti.kernel
def initialize_voxels():
    create_sierpinski_carpet(ivec3(-64, -64, -64), 80, vec3(0.05))

initialize_voxels()

scene.finish()