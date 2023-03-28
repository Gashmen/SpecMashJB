import ezdxf
from ezdxf.addons import Importer


def clear_base_doc_for_new(dxfbase_path:str, dict_for_save_blocks_before_draw:dict):
    '''Удаляем все ненужное из dxf_base
    :dxfbase_path : C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf
    :dict_for_save_blocks_before_draw: {'shell':['VP.121210_cutside',...],
                                        'terminal':['SUPU_SCREW_BLUE_16',...],
                                        'inputs':['VZ-N25_exe,...']}
    '''
    doc_dxfbase = ezdxf.readfile(dxfbase_path)

    doc_dxfbase_for_del = ezdxf.readfile(dxfbase_path)

    doc_dxfbase.modelspace().delete_all_entities()

    block_needed_for_draw = [block_name for i in list(dict_for_save_blocks_before_draw.values()) for block_name in i]

    for block in doc_dxfbase_for_del.blocks:
        try:
            if block.dxf.name not in block_needed_for_draw and '*' not in block.dxf.name:
                    doc_dxfbase.blocks.delete_block(name=block.dxf.name)
        except:
            continue
    return doc_dxfbase

def create_list_with_blocks_in_importer(doc_importer)->list[str]:
    '''Возвращаем список имен блоков в doc'''
    list_with_block_names = [block.dxf.name for block in doc_importer.blocks if '*' not in block.dxf.name]
    return list_with_block_names

def check_block_in_importer_doc(list_with_names_blocks:list[str], block_name:str):
    '''Проверка, есть ли в этом импортере данный блок'''
    if block_name in list_with_names_blocks:
        return True
    else:
        return False

def create_importer(doc_importer,doc_new):
    '''
    :param doc_importer:
    :param doc_new:
    :return:
    '''
    importer = Importer(doc_importer, doc_new)
    return importer

def import_needed_block(importer, list_with_block_names:list[str]):
    '''
    Импортирует необходимые блоки из контейнера по списку, полученному в другом месте
    '''

    for i in list(set(list_with_block_names)):
        importer.import_block(i)
    importer.finalize()

if __name__ == '__main__':
    path_to_base_dxf_files = {
        'shell': 'C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Оболочка\ContainerVer02.dxf',
        'inputs': 'C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Оболочка\ContainerVer02.dxf',
        'terminals' : 'C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Клеммы\checkcheck.dxf'
    }

    '''Создаем необходимые docs для импортирования и добавления блоков'''
    doc_terminals = ezdxf.readfile(path_to_base_dxf_files['terminals'])
    doc_shells = ezdxf.readfile(path_to_base_dxf_files['shell'])
    doc_new_file = ezdxf.new()
    '''Создаем списки блоков, которые есть в контейнерах'''
    list_blocks_terminals_importer = create_list_with_blocks_in_importer(doc_importer=doc_terminals)

    list_blocks_shell_importer = create_list_with_blocks_in_importer(doc_importer=doc_shells)

    dict_importer = {doc_terminals: list_blocks_terminals_importer,
                     doc_shells:list_blocks_shell_importer}

    importer_terminals = create_importer(doc_importer= doc_terminals,
                                         doc_new = doc_new_file
                                         )

    import_needed_block(importer= importer_terminals,
                        list_with_block_names = list_blocks_terminals_importer
                        )

    importer_shells = create_importer(doc_importer = doc_shells,
                                      doc_new = doc_new_file)

    import_needed_block(importer=importer_shells,
                        list_with_block_names=list_blocks_shell_importer
                        )

    doc_new_file.saveas('C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\\testing\\test.dxf')

    '''Создаем списки по каждому листу в приложении'''
    # list_terminals_from_qt = ['SUPU_SCREW_GREEN_16','SUPU_SCREW_GREEN_16','SUPU_SCREW_GREEN_16','SUPU_SCREW_WHITE_16']






