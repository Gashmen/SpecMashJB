import sys
import os
import openpyxl
import ezdxf
from ezdxf.entities import Dimension, Insert
path_to_dxf = 'C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx_dimesion._2.dxf'
doc = ezdxf.readfile(path_to_dxf)
msp = doc.modelspace()

for i in range(5):
    if i == 3:
        continue
    print(i)

#     if isinstance(i, Dimension):
#         print(i.dxf.geometry)
#         i.explode()
#         # for j in i.virtual_entities():
#         #     print(j.dxf.color)
#     # if isinstance(i, Insert):
#     #     for entity in i.query():
#     #         print(entity.dxf.color)
#         # print(i.dxf.name)
#         # i.dxf.dimstyle = 'KDIMSTYLE'
#         # print(i.dxf.dimstyle)
#
# doc.save()



