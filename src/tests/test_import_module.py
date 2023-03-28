import ezdxf
from ezdxf.addons import Importer



doc_for_import = ezdxf.readfile('C:\\Users\g.zubkov\PycharmProjects\FinalProject\src\dxf_base\shells.dxf')
for entity in doc_for_import.modelspace().query():
    if entity.dxftype() == 'INSERT':
        if entity.dxf.name != 'VP.121209_installation_dimensions':
            doc_for_import.modelspace().delete_entity(entity)
    else:
        doc_for_import.modelspace().delete_entity(entity)

list_with_insert_in_block = [i.dxf.name for i in doc_for_import.blocks['VP.121209_installation_dimensions'] if i.dxftype() == 'INSERT']
list_with_insert_in_block.append('VP.121209_installation_dimensions')

for block in doc_for_import.blocks:
    try:
        if block.dxf.name not in  list_with_insert_in_block and '*' not in block.dxf.name:
                doc_for_import.blocks.delete_block(name  = block.dxf.name)
    except:
        continue
doc_for_import.saveas('TEST.dxf')





    #
    # doc_new = ezdxf.new()
    # importer = Importer(doc_importer, doc_new)
    # print(1)