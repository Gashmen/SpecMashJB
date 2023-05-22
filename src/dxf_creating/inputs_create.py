import transliterate
from src.dxf_creating import shell_create
'''
DICT-WITH-INPUTS
{'А': {0: {'ВЗ-Н20': [33.4, 37.5]}, 1: {'ВЗ-Н20': [86.6, 37.5]}},
'Б': {0: {'ВЗ-Н20': [49.0, 37.5]}},
'В': {0: {'ВЗ-Н20': [60.0, 37.5]}}, 'Г': {}, 'Крышка': {}}
'''

def define_shell_type(full_shell_name: str) -> str:
    '''
     :param full_shell_name: VA.161609
     :return: VA.161609
    '''
    return full_shell_name

def define_matching(dict_with_inputs: dict, how_rotation='horizontal') -> dict[str:str]:
    '''
     :param dict_with_inputs:
     {'А': {0: {'ВЗ-Н20': [33.4, 37.5]}, 1: {'ВЗ-Н20': [86.6, 37.5]}},
     'Б': {0: {'ВЗ-Н20': [49.0, 37.5]}},
     'В': {0: {'ВЗ-Н20': [60.0, 37.5]}}, 'Г': {}, 'Крышка': {}}
     :param how_rotation:
     horizontal or vertical
     :return: Возвращает словарь по типу
     {'_upside': {0: {'ВЗ-Н20': [33.4, 37.5]}, 1: {'ВЗ-Н20': [86.6, 37.5]}},
     '_rightside': {0: {'ВЗ-Н20': [49.0, 37.5]}},
     '_downside': {0: {'ВЗ-Н20': [60.0, 37.5]}}, '_leftside': {}, 'Крышка': {}}
     '''
    define_matching_dict = dict()
    for letter in dict_with_inputs.keys():
        if how_rotation == 'horizontal':
            if letter == 'А':
                define_matching_dict['_upside'] = dict_with_inputs[letter]
            elif letter == 'Б':
                define_matching_dict['_rightside'] = dict_with_inputs[letter]
            elif letter == 'В':
                define_matching_dict['_downside'] = dict_with_inputs[letter]
            elif letter == 'Г':
                define_matching_dict['_leftside'] = dict_with_inputs[letter]
            else:
                define_matching_dict[letter] = dict_with_inputs[letter]
        else:
            if letter == 'А':
                define_matching_dict['_rightside'] = dict_with_inputs[letter]
            elif letter == 'Б':
                define_matching_dict['_downside'] = dict_with_inputs[letter]
            elif letter == 'В':
                define_matching_dict['_leftside'] = dict_with_inputs[letter]
            elif letter == 'Г':
                define_matching_dict['_upside'] = dict_with_inputs[letter]
            else:
                define_matching_dict[letter] = dict_with_inputs[letter]

    return define_matching_dict


def translit_input(russian_name_input: str) -> str:
    '''
     Делает транслит
     :param russian_name_input: ВЗ-Н20
     :return: VZ-N20
     '''
    return transliterate.translit(russian_name_input, language_code='ru', reversed=True)


def type_of_explosion_protection(type_explosion='exe') -> str:
    '''Возвращает тип взрывозащиты
     Для добавления к имени Inputs и изменения блока в автокаде(вставки либо exe, либо exd)
     _exe or _exd
     '''
    return '_' + type_explosion


def return_input_name_in_dict(dict_with_input_name_and_coord: dict) -> str:
    '''
     Преорбазует имя в словаре и возравщает только имя
     :param dict_with_input_name_and_coord: {'ВЗ-Н20': [33.4, 37.5]}
     :return: VZ-N20
     '''

    input_name = list(dict_with_input_name_and_coord.keys())[0]
    return translit_input(input_name)


def return_input_coordinate_in_dict(dict_with_input_name_and_coord: dict) -> list:
    '''
     :param dict_with_input_name_and_coord: {'ВЗ-Н20': [33.4, 37.5]}
     :return: [33.4, 37.5]
    '''
    return list(dict_with_input_name_and_coord.values())[0]

    
def create_list_for_drawing_inputs(dict_with_inputs_on_side:dict)->list[str]:
    '''
    :param dict_with_inputs_on_side: {'А': ['ВЗ-Н25','ВЗ-Н25'], 'Б': ['ВЗ-Н25','ВЗ-Н25'],'В': [], 'Г': [],'Крышка': []}
    :return: [VZ-N12_exd,VZ-N12_exe,VZ-N12_withoutcap,VZ-N12_withcap]
    '''

    list_for_drawing_inputs = list()

    end_of_block_name = ['_exd','_exe','_withoutcap','_withcap']

    for list_inputs_rusname_on_side in dict_with_inputs_on_side.values():
        for inputs_rusname_on_side in list_inputs_rusname_on_side:
            list_for_drawing_inputs.append(translit_input(inputs_rusname_on_side))

    list_for_drawing_inputs = list(set(list_for_drawing_inputs))

    return_list = list()

    for translate_name in list_for_drawing_inputs:
        for end_name in end_of_block_name:
            return_list.append(translate_name + end_name)

    return return_list

def create_inputs_in_block(doc, dict_before_match: dict, full_shale_name:str, type_of_explosion='exe'):
    '''
     Добавление вводов в блоки на каждый вид(добавляется в сам блок)
     dict_after_match = define_matching()
     dict_before_match = {'А': {0: {'ВЗ-Н25': [32.11666666666667, 37.5]}, 1: {'ВЗ-Н25': [87.88333333333333, 37.5]}},
        'Б': {0: {'ВЗ-Н25': [24.783333333333335, 37.5]}, 1: {'ВЗ-Н25': [73.21666666666667, 37.5]}},
        'В': {},
        'Г': {},
        'Крышка': {}}
     full_shale_name = VP.110806
     type_of_explosion = exe or exd
     '''
    shale_name = define_shell_type(full_shale_name)
    dict_after_match = define_matching(dict_before_match, how_rotation='horizontal')
    for side, dict_with_inputs in dict_after_match.items():
        if dict_with_inputs:
            for input_number, dict_with_diametr_and_coordinate in dict_with_inputs.items():
                input_name = return_input_name_in_dict(dict_with_diametr_and_coordinate) + \
                             type_of_explosion_protection(type_of_explosion)

                input_coordinate = return_input_coordinate_in_dict(dict_with_diametr_and_coordinate)

                doc.blocks[f'{shale_name}{side}'].add_blockref(input_name, input_coordinate)

    return doc

def create_inputs_on_topside_withoutcapside(doc,shell_name:str):
    '''
    Создаем inputs вокруг блока topside и вокруг блока withoutcapside
    :param doc:
    :param shell_name: VP.161610
    :return:doc_new
    '''
    sides = ['_rightside','_leftside','_downside','_upside']

    insert_topside = doc.modelspace().query(f'INSERT[name == "{shell_name}_topside"]')[0]
    topside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_topside)

    insert_withoutcapside = doc.modelspace().query(f'INSERT[name == "{shell_name}_withoutcapside"]')[0]
    withoutcapside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_withoutcapside)


    for side in sides:
        for inputs_insert in doc.modelspace().query(f'INSERT[name == "{shell_name}{side}"]')[0].virtual_entities():
            if inputs_insert.dxftype() =='INSERT':
                input_name = inputs_insert.dxf.name.split('_')[0]
                if side == '_downside':
                    input_downside_on_topside = doc.modelspace().add_blockref(
                                                                   name=input_name  + '_withoutcap',
                                                                   insert=(list(inputs_insert.dxf.insert)[0],
                                                                           topside_extreme_lines['y_max']))
                    input_downside_on_topside.dxf.rotation = 180

                    input_downside_on_withoutcapside = doc.modelspace().add_blockref(
                                                                        name=input_name + '_withcap',
                                                                        insert=(list(inputs_insert.dxf.insert)[0] + withoutcapside_extreme_lines['xy_0'][0],
                                                                                withoutcapside_extreme_lines['y_max']))
                    input_downside_on_withoutcapside.dxf.rotation = 180


                elif side == '_upside':
                    input_upside_on_topside = doc.modelspace().add_blockref(name=input_name  + '_withoutcap',
                                                  insert=(list(inputs_insert.dxf.insert)[0],
                                                          topside_extreme_lines['y_min']))
                    input_upside_on_topside.dxf.rotation = 0

                    input_upside_on_withoutcapside = doc.modelspace().add_blockref(name=input_name + '_withcap',
                                                                 insert=(list(inputs_insert.dxf.insert)[0] + withoutcapside_extreme_lines['xy_0'][0],
                                                                         withoutcapside_extreme_lines['y_min']))
                    input_upside_on_withoutcapside.dxf.rotation = 0


                elif side == '_rightside':
                    input_rightside_on_topside = doc.modelspace().add_blockref(name=input_name  + '_withoutcap',
                                                  insert = (topside_extreme_lines['x_max'],
                                                            list(inputs_insert.dxf.insert)[1]))
                    input_rightside_on_topside.dxf.rotation = 90

                    input_rightside_on_withoutcapside = doc.modelspace().add_blockref(name=input_name + '_withcap',
                                                                               insert=(withoutcapside_extreme_lines['x_max'],
                                                                                       list(inputs_insert.dxf.insert)[
                                                                                           1]))
                    input_rightside_on_withoutcapside.dxf.rotation = 90


                elif side == '_leftside':
                    input_leftside_on_topside = doc.modelspace().add_blockref(name=input_name  + '_withoutcap',
                                                  insert = (topside_extreme_lines['x_min'],
                                                            list(inputs_insert.dxf.insert)[1]))
                    input_leftside_on_topside.dxf.rotation = 270

                    input_leftside_on_withoutcapside = doc.modelspace().add_blockref(name=input_name + '_withcap',
                                                                   insert=(withoutcapside_extreme_lines['x_min'],
                                                                           list(inputs_insert.dxf.insert)[1]))
                    input_leftside_on_withoutcapside.dxf.rotation = 270

