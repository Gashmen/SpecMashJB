import ezdxf

import src.dxf_creating.measure_block as measure_block
import src.dxf_creating.shell_create as shell_create
from src.dxf_creating import CONST, search_len_block

def check_din_reyka(doc, shell_name:str):
    '''Проверка наличия дин рейки в doc
    shell_name вида VP.110806
    '''
    for insert in doc.modelspace().query('INSERT'):
        if insert.dxf.name == f'DIN_{shell_name}':
            return insert
    return False


def return_terminal_block(doc,list_with_terminal:list[str]):
    '''
    Получение блоков клемм из doc
    :param doc: doc после импорта необходимых клемм
    :list_with_terminal:list[str]: Список клемм по именам, которые добавляют
    :return: list с блоками клемм
    '''



def change_name_from_to(name:str):
    '''
    Смена имени для клеммы с английского на русский и наоборот по структуре на 06.02.23
    '''
    const_names = {'Концевой стопор':'Terminal_end_stop_frontside',
                   'Концевая пластина':'Terminal_end_plate_frontside_2.5'}
    if name in list(const_names.keys()):
        return const_names[name]


    return_name = name
    rus_language = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    #Проверка если есть русские буквы в строке, то значит это приход
    dict_translator = {'Винтовые':'SCREW','Пружинные':'SPRING', 'PE':'GREEN','L':'WHITE','N':'BLUE',
                       }
    rus = None
    for letter in name.lower():
        if letter in rus_language:
            rus = True
            break
    if rus == None:
        dict_eng = {eng_word:rus_word for rus_word,eng_word in dict_translator}
        for word_eng in dict_eng.keys():
            if word_eng in return_name:
                return_name.replace(word_eng,dict_eng[word_eng])
    else:
        return_name = return_name.split('_')
        for word_rus in dict_translator:
            if word_rus in return_name:
                return_name[return_name.index(word_rus)] = dict_translator[word_rus]
        return_name = '_'.join(return_name)
    return return_name

def create_list_for_drawing_terminal(list_with_terminal:list)->list[str]:
    '''
    Создает импорт лист для клемм
    :param list_with_terminal: ['SUPU_Винтовые_PE_16','Концевая пластина','Концевой стопор','SUPU_Винтовые_L_16' ]
    :return: return_list : ['SUPU_SCREW_GREEN_16',...]
    '''
    list_for_import =[*list(set(list_with_terminal))]
    for type_terminal in list_for_import.copy():
        list_for_import.append(type_terminal + '_viewside')


    list_for_import.append('Terminal_end_stop_frontside')
    list_for_import.append('Terminal_end_stop_viewside')
    list_for_import.append('Terminal_end_plate_frontside_2.5')
    list_for_import.append('Terminal_end_plate_frontside_16')

    return list_for_import


def check_importers_docs(path_to_terminal = None, path_to_end = None,list_with_terminal:list = None )->list:
    '''
    :param path_to_terminal: C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Клеммы\checkcheck.dxf
    :param path_to_end: C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Клеммы\End_stop.dxf
    :return: [doc_for_terminals,doc_for_end]
    '''

    list_with_terminal_docs = list()
    counter = 0
    if path_to_terminal is not None:
        doc_terminal = ezdxf.readfile(path_to_terminal)

        for block_terminal in doc_terminal.blocks:
            if block_terminal.dxf.name == 'Terminal_end_stop_frontside':
                list_with_terminal_docs.append(doc_terminal)
                counter +=1
                break

    if path_to_end is not None and counter !=0:
        doc_end = ezdxf.readfile(path_to_end)
        list_with_terminal_docs.append(doc_end)

    return list_with_terminal_docs

def return_blocks_names(doc)->list[str]:
    '''
    Возвращает список имен в doc
    :param doc:
    :return:
    '''
    list_names_block = list()
    for block in doc.blocks:
        if '*' not in block.dxf.name:
            list_names_block.append(block.dxf.name)
    return list_names_block

def check_blocks_names_in_doc(list_docs = None,list_for_import = None)->list[str]:
    '''
    Проверка есть ли имена необходимых блоков в doc
    :param list_docs:[docs_terminal, docs_end,...]
    :param list_for_import:['SUPU_SCREW_GREEN_16',...]
    :return:
    '''
    list_for_deliting = list_for_import.copy()
    if list_docs is not None:
        for doc in list_docs:
            doc_block_names = return_blocks_names(doc = doc)
            if list(set(list_for_import)&set(doc_block_names)) == list_for_import:
                return True


def define_len_terminal(doc_after_import, terminal_name_in_doc:str)->float:
    '''определяет горизонтальную длину клеммы '''
    '''РАБОТАЕТ!!!!!'''
    block_terminal = doc_after_import.blocks[terminal_name_in_doc]

    return measure_block.calculate_horizontal_len_block(block=block_terminal)


def calculate_sum_len_terminal(doc_after_import,list_with_terminal:list):
    '''Расчет суммарной длины клемм
    doc_after_import: doc, в который добавили уже и клеммы
    list_with_terminal: Значение с list_widget ['SUPU_Винтовые_PE_16','Концевая пластина',
                                                'Концевой стопор','SUPU_Винтовые_L_16' ]
    '''
    pass

def set_hatch_before_entity(block):
    '''
    Вынос наперед заливки
    :param block:
    :return:
    '''
    block.set_redraw_order(
        (solid.dxf.handle, "%X" % (200 - solid.dxf.color))
        for solid in block.entity_space if solid.dxftype() == 'HATCH')

def create_terminal_on_din(doc_after_import, list_terminal_blocks, din_reyka_insert):
    '''Создать клеммы на дин рейке
    doc_after_import: doc, в который добавили уже и клеммы
    list_with_terminal: Значение с list_widget ['SUPU_Винтовые_PE_16','Концевая пластина',
                                                'Концевой стопор','SUPU_Винтовые_L_16' ]
    din_reyka_insert: insert Дин рейки уже на моделспейсе
    '''
    summary_terminal_len = sum([define_len_terminal(doc_after_import, terminal)
                                for terminal in list_terminal_blocks])

    din_reyka_insert_coordinate = [din_reyka_insert.dxf.insert[0],din_reyka_insert.dxf.insert[1]]

    x_first_coordinate = din_reyka_insert_coordinate[0] - summary_terminal_len/2
    y_first_coordinate = din_reyka_insert_coordinate[1]



    for terminal_name in list_terminal_blocks:
        #Работаем с hatch
        # block_terminal = doc_after_import.blocks[terminal_name]
        # set_hatch_before_entity(block=block_terminal)

        len_terminal = define_len_terminal(doc_after_import,terminal_name)
        x_insert = x_first_coordinate + len_terminal/2
        y_insert = y_first_coordinate
        doc_after_import.modelspace().add_blockref(terminal_name,
                                                   insert=(x_insert,y_insert))
        x_first_coordinate += len_terminal
    return doc_after_import

def create_terminal_on_cutside(doc_after_terminal, list_terminal_blocks:list[str], shell_name:str):
    '''
    Создать клеммы в разрезе
    :param doc_after_terminal: doc, в котором добавили клеммы на withoutcapside
    :param list_terminal_blocks: Значение с list_widget ['SUPU_Винтовые_PE_16','Концевая пластина',
                                                        'Концевой стопор','SUPU_Винтовые_L_16' ]
    :param shell_name: VP.161610
    :return:
    '''

    din_block = doc_after_terminal.blocks['35_DIN_CUTSIDE']
    len_din = max(search_len_block.create_dict_with_vertical_lines(din_block).keys())

    cutside_insert = doc_after_terminal.modelspace().query(f'INSERT[name=="{shell_name}_cutside"]')[0]

    withoutcapside_insert = doc_after_terminal.modelspace().query(f'INSERT[name=="{shell_name}_withoutcapside"]')[0]
    withoutcapside_extreme_lines = shell_create.define_extreme_lines_in_insert(withoutcapside_insert)

    list_terminal_blocks = [insert_terminal.dxf.name for insert_terminal in doc_after_terminal.modelspace().query(f'INSERT')
                            if (insert_terminal.dxf.insert[0] > withoutcapside_insert.dxf.insert[0]) and\
                            (withoutcapside_extreme_lines['y_min'] < insert_terminal.dxf.insert[1] < withoutcapside_extreme_lines['y_max'])
                            if ('WHITE' in insert_terminal.dxf.name or 'BLUE' in insert_terminal.dxf.name or 'GREEN' in insert_terminal.dxf.name)]

    coordinate_din_in_cutside = doc_after_terminal.blocks[
                                   f'{shell_name}_cutside'].query('INSERT[name=="35_DIN_CUTSIDE"]')[0].dxf.insert



    for terminal in list_terminal_blocks.copy()[::-1]:
        if terminal != 'Terminal_end_plate_frontside_2.5':
            if terminal != 'Terminal_end_stop_frontside':

                doc_after_terminal.modelspace().add_blockref(name=f'{terminal}_viewside',
                                                            insert=(cutside_insert.dxf.insert[0] +
                                                                    coordinate_din_in_cutside[1] + len_din,
                                                                    cutside_insert.dxf.insert[1] -
                                                                    coordinate_din_in_cutside[0])
                                                             )
            else:
                doc_after_terminal.modelspace().add_blockref(name="Terminal_end_stop_viewside",
                                                             insert=(cutside_insert.dxf.insert[0] +
                                                                     coordinate_din_in_cutside[1] + len_din,
                                                                     cutside_insert.dxf.insert[1] -
                                                                     coordinate_din_in_cutside[0])
                                                             )
    return doc_after_terminal




def create_terminal(doc_after_import):
    '''Добавляет в doc_after_import клеммы'''
    pass

# def create_terminals(doc,shell_name:str,list_with_terminals):
















