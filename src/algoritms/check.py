import ezdxf
from ezdxf.addons import Importer


doc = ezdxf.readfile('C:\\Users\g.zubkov\PycharmProjects\FinalProject\src\\xx.dxf')
msp = doc.modelspace()

for entity in doc.blocks['VP.110806_installation_dimensions']:
    if entity.dxftype() == 'DIMENSION':
        for i in entity.virtual_entities():
            if i.dxftype() == "LINE":
                print(i.dxf.end)
            print(i)

    # print(entity.dxftype())
