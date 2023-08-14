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
    if input_name == 'Устройство заземления':
        return "ground"
    else:
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
            if inputs_rusname_on_side == "Устройство заземления":
                list_for_drawing_inputs.append('ground')
            else:
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
    inputs_insert_on_topside = {'_rightside':{},'_leftside':{},'_downside':{},'_upside':{}}

    insert_withoutcapside = doc.modelspace().query(f'INSERT[name == "{shell_name}_withoutcapside"]')[0]
    withoutcapside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_withoutcapside)

    insert_downside = doc.modelspace().query(f'INSERT[name == "{shell_name}_downside"]')[0]
    downside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_downside)

    insert_upside = doc.modelspace().query(f'INSERT[name == "{shell_name}_upside"]')[0]
    upside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_upside)

    insert_rightside = doc.modelspace().query(f'INSERT[name == "{shell_name}_rightside"]')[0]
    rightside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_rightside)

    insert_leftside = doc.modelspace().query(f'INSERT[name == "{shell_name}_leftside"]')[0]
    leftside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_leftside)

    insert_cutside = doc.modelspace().query(f'INSERT[name == "{shell_name}_cutside"]')[0]
    cutside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_cutside)

    for side in sides:
        for inputs_insert in doc.modelspace().query(f'INSERT[name == "{shell_name}{side}"]')[0].virtual_entities():
            if inputs_insert.dxftype() =='INSERT':
                input_name = inputs_insert.dxf.name.split('_')[0]
                if side == '_upside':
                    input_downside_on_topside = doc.modelspace().add_blockref(
                                                                   name=input_name + '_withoutcap',
                                                                   insert=(list(inputs_insert.dxf.insert)[0],
                                                                           topside_extreme_lines['y_max']))
                    input_downside_on_topside.dxf.rotation = 180

                    input_downside_on_withoutcapside = doc.modelspace().add_blockref(
                                                                        name=input_name + '_withcap',
                                                                        insert=(list(inputs_insert.dxf.insert)[0] + withoutcapside_extreme_lines['xy_0'][0],
                                                                                withoutcapside_extreme_lines['y_max']))
                    input_downside_on_withoutcapside.dxf.rotation = 180

                    inputs_insert_height = upside_extreme_lines['y_max'] - inputs_insert.dxf.insert[1]
                    inputs_insert_on_topside[side][input_downside_on_topside] = inputs_insert_height

                elif side == '_downside':
                    input_upside_on_topside = doc.modelspace().add_blockref(name=input_name  + '_withoutcap',
                                                  insert=(list(inputs_insert.dxf.insert)[0],
                                                          topside_extreme_lines['y_min']))
                    input_upside_on_topside.dxf.rotation = 0

                    input_upside_on_withoutcapside = doc.modelspace().add_blockref(name=input_name + '_withcap',
                                                                 insert=(list(inputs_insert.dxf.insert)[0] + withoutcapside_extreme_lines['xy_0'][0],
                                                                         withoutcapside_extreme_lines['y_min']))
                    input_upside_on_withoutcapside.dxf.rotation = 0

                    inputs_insert_height = inputs_insert.dxf.insert[1] - downside_extreme_lines['y_min']
                    inputs_insert_on_topside[side][input_upside_on_topside] = inputs_insert_height

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

                    inputs_insert_height = rightside_extreme_lines['x_max'] - inputs_insert.dxf.insert[0]
                    inputs_insert_on_topside[side][input_rightside_on_topside] = inputs_insert_height


                elif side == '_leftside':
                    input_leftside_on_topside = doc.modelspace().add_blockref(name=input_name  + '_withoutcap',
                                                  insert = (topside_extreme_lines['x_min'],
                                                            list(inputs_insert.dxf.insert)[1]))
                    input_leftside_on_topside.dxf.rotation = 270

                    input_leftside_on_withoutcapside = doc.modelspace().add_blockref(name=input_name + '_withcap',
                                                                   insert=(withoutcapside_extreme_lines['x_min'],
                                                                           list(inputs_insert.dxf.insert)[1]))
                    input_leftside_on_withoutcapside.dxf.rotation = 270

                    inputs_insert_height = inputs_insert.dxf.insert[0] - leftside_extreme_lines['x_min']
                    inputs_insert_on_topside[side][input_leftside_on_topside] = inputs_insert_height



    #Обрабатываем inputs_insert_on_topside
    for side in inputs_insert_on_topside.copy():
        if side == '_upside' or side == '_downside':
            inputs_insert_on_topside[side] = dict(
                sorted(inputs_insert_on_topside[side].items(), key=lambda x: x[0].dxf.insert[0], reverse=False))
            for input_on_topside in inputs_insert_on_topside[side].keys():
                input_on_rightside = doc.modelspace().add_blockref(
                    name=input_on_topside.dxf.name,
                    insert=(rightside_extreme_lines['x_max'] - inputs_insert_on_topside[side][input_on_topside],
                            input_on_topside.dxf.insert[1])
                )
                if side == '_upside':
                    input_on_rightside.dxf.rotation = 180
                else:
                    input_on_rightside.dxf.rotation = 0
            inputs_insert_on_topside[side] = dict(
                sorted(inputs_insert_on_topside[side].items(), key=lambda x: x[0].dxf.insert[0], reverse=True))
            for input_on_topside in inputs_insert_on_topside[side].keys():
                input_on_leftside = doc.modelspace().add_blockref(
                    name=input_on_topside.dxf.name,
                    insert=(leftside_extreme_lines['x_min'] + inputs_insert_on_topside[side][input_on_topside],
                            input_on_topside.dxf.insert[1])
                )
                if side == '_upside':
                    input_on_leftside.dxf.rotation = 180
                else:
                    input_on_leftside.dxf.rotation = 0

                # input_on_cutside = doc.modelspace().add_blockref(
                #     name=input_on_topside.dxf.name,
                #     insert=(cutside_extreme_lines['x_max'] + inputs_insert_on_topside[side][input_on_topside],
                #             input_on_topside.dxf.insert[1]))
            inputs_insert_on_topside[side] = dict(
                sorted(inputs_insert_on_topside[side].items(), key=lambda x: x[0].dxf.insert[0], reverse=True))
            for i in inputs_insert_on_topside[side].copy():
                if i.dxf.insert[0] < insert_topside.dxf.insert[0]:
                    inputs_insert_on_topside[side].pop(i)

            for input_on_topside in inputs_insert_on_topside[side].keys():
                input_on_leftside = doc.modelspace().add_blockref(
                    name=input_on_topside.dxf.name,
                    insert=(cutside_extreme_lines['x_min'] + inputs_insert_on_topside[side][input_on_topside],
                            input_on_topside.dxf.insert[1])
                )
                if side == '_upside':
                    input_on_leftside.dxf.rotation = 180
                else:
                    input_on_leftside.dxf.rotation = 0

        if side == '_leftside' or side == '_rightside':
            inputs_insert_on_topside[side] = dict(
                sorted(inputs_insert_on_topside[side].items(), key=lambda x: x[0].dxf.insert[1], reverse=False))
            for input_on_topside in inputs_insert_on_topside[side].keys():
                input_on_upside = doc.modelspace().add_blockref(
                    name=input_on_topside.dxf.name,
                    insert=(input_on_topside.dxf.insert[0],
                            upside_extreme_lines['y_max'] - inputs_insert_on_topside[side][input_on_topside])
                )
                if side == '_leftside':
                    input_on_upside.dxf.rotation = 270
                else:
                    input_on_upside.dxf.rotation = 90
            inputs_insert_on_topside[side] = dict(
                sorted(inputs_insert_on_topside[side].items(), key=lambda x: x[0].dxf.insert[1], reverse=True))
            for input_on_topside in inputs_insert_on_topside[side].keys():
                input_on_downside = doc.modelspace().add_blockref(
                    name=input_on_topside.dxf.name,
                    insert=(input_on_topside.dxf.insert[0],
                            downside_extreme_lines['y_min'] + inputs_insert_on_topside[side][input_on_topside])
                )
                if side == '_leftside':
                    input_on_downside.dxf.rotation = 270
                else:
                    input_on_downside.dxf.rotation = 90



def create_needed_elements_cutside(doc,shell_name,max_input_length):
    '''
    Создаем обозначение разреза
    :param doc:
    :param shell_name: VP.161610
    :return:doc_new
    '''

    insert_topside = doc.modelspace().query(f'INSERT[name == "{shell_name}_topside"]')[0]
    topside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_topside)

    insert_downside = doc.modelspace().query(f'INSERT[name == "{shell_name}_downside"]')[0]
    downside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_downside)

    insert_upside = doc.modelspace().query(f'INSERT[name == "{shell_name}_upside"]')[0]
    upside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_upside)

    insert_cutside = doc.modelspace().query(f'INSERT[name == "{shell_name}_cutside"]')[0]
    cutside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_cutside)

    list_inserts_top = []
    list_inserts_bottom = []

    for insert_inputs in doc.modelspace().query(f'INSERT'):
        if shell_name not in insert_inputs.dxf.name:
            x_input = insert_inputs.dxf.insert[0]
            y_input = insert_inputs.dxf.insert[1]
            if (insert_topside.dxf.insert[0] < x_input < topside_extreme_lines['x_max']) and\
                (topside_extreme_lines['y_max'] <= y_input < downside_extreme_lines['y_min']):
                list_inserts_top.append(insert_inputs)
            elif (insert_topside.dxf.insert[0] < x_input < topside_extreme_lines['x_max']) and\
                (upside_extreme_lines['y_max'] < y_input <= topside_extreme_lines['y_min']):
                list_inserts_bottom.append(insert_inputs)


    list_inserts_top = sorted(list_inserts_top, key=lambda x: x.dxf.insert[0], reverse=False)
    list_inserts_bottom = sorted(list_inserts_bottom, key=lambda x: x.dxf.insert[0], reverse=False)

    for input_on_topside in list_inserts_top:
        input_on_rightside = doc.modelspace().add_blockref(
            name=input_on_topside.dxf.name,
            insert=(rightside_extreme_lines['x_max'] - inputs_insert_on_topside[side][input_on_topside],
                    input_on_topside.dxf.insert[1])
        )
        if side == '_upside':
            input_on_rightside.dxf.rotation = 180


    insert_cutside = doc.modelspace().query(f'INSERT[name == "{shell_name}_cutside"]')[0]
    cutside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_leftside)
