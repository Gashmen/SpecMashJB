import os
import ezdxf
from ezdxf.addons import Importer

from src.dxf_creating import shell_create,inputs_create,inputs_on_shell




def import_needed_block(importer, list_with_block_names):
    '''
    Импортирует необходимые блоки из контейнера по списку, полученному в другом месте
    '''
    for i in list_with_block_names:
        importer.import_block(i)
    importer.finalize()

def new_doc_create(path_to_library_dxf_with_shell, list_for_import,version_dxf = 'AC1024'):
    '''
    :param path_to_library_dxf_with_shell: os.getcwd() + \\foldername\\База
    :param list_for_import: ['VP.161610_topside',.....]
    :param version_dxf: версия dxf
    :return: doc_new
    '''
    doc = ezdxf.readfile(path_to_library_dxf_with_shell)
    doc_new_file = ezdxf.new(dxfversion=version_dxf)
    importer = Importer(doc,doc_new_file)
    import_needed_block(importer=importer,
                        list_with_block_names=list_for_import)
    return doc_new_file

def search_inputs_on_topside(doc,shell_name:str)->dict:
    '''
    :param doc: Doc после добавления вводов на topside
    :return: Получение словаря с координатами по каждому вводу
    {0:[INSERT1,INSERT2....],90:[],180:[],270:[]}
    Ключ будет поворотом, а значение список с INSERTS
    '''
    inputs_on_topside = {0:[],90:[],180:[],270:[]}
    topside_extreme_lines = shell_create.define_extreme_lines_in_insert(shell_create.topside_insert(doc,shell_name))
    for insert_withoutcap in doc.modelspace().query('INSERT'):
        if insert_withoutcap.dxf.name.endswith('withoutcap'):
            '''Поиск верхнего и нижнего ввода INSERT который находится на topside'''
            if insert_withoutcap.dxf.rotation == 180 or insert_withoutcap.dxf.rotation == 0:
                x_coordinate_insert = insert_withoutcap.dxf.insert[0]
                y_coordinate_insert = insert_withoutcap.dxf.insert[1]

                if topside_extreme_lines['x_min'] < x_coordinate_insert < topside_extreme_lines['x_max']:
                    inputs_on_topside[insert_withoutcap.dxf.rotation].append(insert_withoutcap)
            #Поиск левого и правого ввода
            elif insert_withoutcap.dxf.rotation == 90 or insert_withoutcap.dxf.rotation == 270:
                x_coordinate_insert = insert_withoutcap.dxf.insert[0]
                y_coordinate_insert = insert_withoutcap.dxf.insert[1]
                if topside_extreme_lines['y_min'] < x_coordinate_insert < topside_extreme_lines['y_max']:
                    inputs_on_topside[insert_withoutcap.dxf.rotation].append(insert_withoutcap)
    return inputs_on_topside

def define_biggest_coordinate_input_on_side(rotation_of_input:int,list_with_insert_inputs:list)-> dict[str:float]:

    '''
    :param rotation: int: 0,90,180 or 270
    :param list_with_insert_inputs: [INSERT1,INSERT2....]
    :return: needed_coordinate_for_move : float: x_max or x_min or y_max or y_min
    '''

    if rotation_of_input == 0:
        min_y = None
        for insert in list_with_insert_inputs:
            if min_y:
                min_y = min(min_y,shell_create.define_extreme_lines_in_insert(insert = insert)['y_min'])
            else:
                min_y = shell_create.define_extreme_lines_in_insert(insert = insert)['y_min']
        return {'y_min' : min_y}

    elif rotation_of_input == 180:
        max_y = None
        for insert in list_with_insert_inputs:
            if max_y:
                max_y = max(max_y, shell_create.define_extreme_lines_in_insert(insert=insert)['y_max'])
            else:
                max_y = shell_create.define_extreme_lines_in_insert(insert=insert)['y_max']
        return {'y_max' :max_y}

    elif rotation_of_input == 270:
        min_x = None
        for insert in list_with_insert_inputs:
            if min_x:
                min_x = max(min_x, shell_create.define_extreme_lines_in_insert(insert=insert)['x_min'])
            else:
                min_x = shell_create.define_extreme_lines_in_insert(insert=insert)['x_min']
        return {'x_min' :min_x}

    elif rotation_of_input == 90:
        max_x = None
        for insert in list_with_insert_inputs:
            if max_x:
                max_x = max(max_x, shell_create.define_extreme_lines_in_insert(insert=insert)['x_max'])
            else:
                max_x = shell_create.define_extreme_lines_in_insert(insert=insert)['x_max']
        return {'x_max' : max_x}

def move_shells_after_inputs_on_topside(doc,inputs_on_topside):

    '''
    :param doc: Док, после вставки вводов на topside
    :param inputs_on_topside:
    {0: [],
    90: [],
    180: [<class 'ezdxf.entities.insert.Insert'> INSERT(#CBC)],
    270: [<class 'ezdxf.entities.insert.Insert'> INSERT(#CBE)]}
    :return: doc, там будут подвинутые оболочки относительно кабельнных вводов
    '''

    #Ниже по факту написано так, что на 180 градусов повернуты shell, для того, чтобы сделать соответствие
    shell_rotation_inputs_change_on_180 = {180:'downside',
                                           0:'upside',
                                           270:'rightside',
                                           90:'leftside'}

    for insert_shells in doc.modelspace().query('INSERT'):
        for shell_rotation, shell_ends_names in shell_rotation_inputs_change_on_180.items():
            if insert_shells.dxf.name.endswith(shell_ends_names):
                list_inputs = inputs_on_topside[shell_rotation]
                dict_with_biggest_coord = define_biggest_coordinate_input_on_side(rotation_of_input=shell_rotation,
                                                                                  list_with_insert_inputs= list_inputs)
                dict_with_coord_insert = shell_create.define_extreme_lines_in_insert(insert=insert_shells)
                if dict_with_biggest_coord.get('x_min',None):
                    insert_shells.dxf.insert = \
                    (insert_shells.dxf.insert[0] - (dict_with_coord_insert['x_max'] - dict_with_biggest_coord['x_min']),
                                                insert_shells.dxf.insert[1])
                elif dict_with_biggest_coord.get('x_max',None):
                    insert_shells.dxf.insert = \
                    (insert_shells.dxf.insert[0] + (dict_with_biggest_coord['x_max'] - dict_with_coord_insert['x_min']),
                                                insert_shells.dxf.insert[1])
                elif dict_with_biggest_coord.get('y_min',None):
                    insert_shells.dxf.insert = \
                        (insert_shells.dxf.insert[0],
                            insert_shells.dxf.insert[1] - (dict_with_coord_insert['y_max'] -  dict_with_biggest_coord['y_min']))
                elif dict_with_biggest_coord.get('y_max',None):
                    insert_shells.dxf.insert = \
                    (insert_shells.dxf.insert[0],
                        insert_shells.dxf.insert[1] + (dict_with_biggest_coord['y_max'] - dict_with_coord_insert['y_min']))
    return doc

def lateral_input_on_side(doc,shell_name,dict_after_matching):

    '''
    :param doc: doc после установки вводов на topside
    :param inputs_on_topside:
    {0: [],
    90: [],
    180: [<class 'ezdxf.entities.insert.Insert'> INSERT(#CBC)],
    270: [<class 'ezdxf.entities.insert.Insert'> INSERT(#CBE)]}
    :param shell_name: 'VP.161610'
    :param dict_after_matching:
    {'А': {0: {'ВЗ-Н20': [33.4, 37.5]}, 1: {'ВЗ-Н20': [86.6, 37.5]}},
     'Б': {0: {'ВЗ-Н20': [49.0, 37.5]}},
     'В': {0: {'ВЗ-Н20': [60.0, 37.5]}}, 'Г': {}, 'Крышка': {}}
    :return: doc с вставленными вбок вводами
    '''

    for side_ABCD, dict_with_key_input in dict_after_matching.items():
        if dict_with_key_input:
            if side_ABCD == '_upside':
                left_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_leftside"]')[0]
                right_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_rightside"]')[0]
                cut_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_cutside"]')[0]
                extreme_lines_leftside = shell_create.define_extreme_lines_in_insert(left_side_insert)
                extreme_lines_rightside = shell_create.define_extreme_lines_in_insert(right_side_insert)
                extreme_lines_cutside = shell_create.define_extreme_lines_in_insert(cut_side_insert)
                for count, dict_with_input in dict_with_key_input.items():
                    input_name = inputs_create.return_input_name_in_dict(dict_with_input_name_and_coord=dict_with_input)
                    coord_input = [coord for coord in list(dict_with_input.values())[0]]

                    leftside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert = (left_side_insert.dxf.insert[0] + coord_input[1],
                                                           extreme_lines_leftside['y_max']))
                    leftside_input.dxf.rotation = 180
                    rightside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert=(right_side_insert.dxf.insert[0] - coord_input[1],
                                                         extreme_lines_rightside['y_max']))
                    rightside_input.dxf.rotation = 180
                    cutside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert=(cut_side_insert.dxf.insert[0] - coord_input[1],
                                                         extreme_lines_cutside['y_max']))
                    cutside_input.dxf.rotation = 180



            if side_ABCD == '_downside':
                left_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_leftside"]')[0]
                right_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_rightside"]')[0]
                extreme_lines_leftside = shell_create.define_extreme_lines_in_insert(left_side_insert)
                extreme_lines_rightside = shell_create.define_extreme_lines_in_insert(right_side_insert)

                for count, dict_with_input in dict_with_key_input.items():
                    input_name = inputs_create.return_input_name_in_dict(dict_with_input_name_and_coord=dict_with_input)
                    coord_input = [coord for coord in list(dict_with_input.values())[0]]

                    leftside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert = (left_side_insert.dxf.insert[0] - coord_input[1],
                                                           extreme_lines_leftside['y_min']))
                    leftside_input.dxf.rotation = 0
                    rightside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert=(right_side_insert.dxf.insert[0] + coord_input[1],
                                                         extreme_lines_rightside['y_min']))
                    rightside_input.dxf.rotation = 0

            if side_ABCD == '_rightside':
                up_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_upside"]')[0]
                down_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_downside"]')[0]
                extreme_lines_upside = shell_create.define_extreme_lines_in_insert(up_side_insert)
                extreme_lines_downside = shell_create.define_extreme_lines_in_insert(down_side_insert)

                for count, dict_with_input in dict_with_key_input.items():
                    input_name = inputs_create.return_input_name_in_dict(dict_with_input_name_and_coord=dict_with_input)
                    coord_input = [coord for coord in list(dict_with_input.values())[0]]

                    upside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert = (extreme_lines_upside['x_max'],
                                                           up_side_insert.dxf.insert[1] - coord_input[1]))
                    upside_input.dxf.rotation = 90
                    downside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                                    insert=(extreme_lines_downside['x_max'],
                                                                            down_side_insert.dxf.insert[1] + coord_input[1]))
                    downside_input.dxf.rotation = 90

            if side_ABCD == '_leftside':
                up_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_upside"]')[0]
                down_side_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_downside"]')[0]
                extreme_lines_upside = shell_create.define_extreme_lines_in_insert(up_side_insert)
                extreme_lines_downside = shell_create.define_extreme_lines_in_insert(down_side_insert)

                for count, dict_with_input in dict_with_key_input.items():
                    input_name = inputs_create.return_input_name_in_dict(dict_with_input_name_and_coord=dict_with_input)
                    coord_input = [coord for coord in list(dict_with_input.values())[0]]

                    upside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                 insert = (extreme_lines_upside['x_min'],
                                                           up_side_insert.dxf.insert[1] - coord_input[1]))
                    upside_input.dxf.rotation = 270
                    downside_input = doc.modelspace().add_blockref(input_name + '_withoutcap',
                                                                    insert=(extreme_lines_downside['x_min'],
                                                                            down_side_insert.dxf.insert[1] + coord_input[1]))
                    downside_input.dxf.rotation = 270

if __name__ == '__main__':

    list_for_import = ['VP.161610_withoutcapside', 'VP.161610_downside', 'VP.161610_cutside',
                       'Border_A3', 'VP.161610_installation_dimensions', 'VZ-N16_withoutcap',
                       'VZ-N20_withoutcap', 'VP.161610_leftside', 'VP.161610_topside',
                       'VZ-N20_withcap', 'VP.161610_upside', 'VP.161610_rightside',
                       'VZ-N20_exe', 'VZ-N20_exd', 'VZ-N20_withcap',
                       'VZ-N16_exe', 'VZ-N16_exd', 'DIN_VP.161610']

    path_to_save = '\\'.join(os.getcwd().split('\\')[0:-1])
    full_library_path = '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\Оболочка\\ContainerVer02.dxf'
    shell_name = 'VP.161610'
    doc_new = new_doc_create(path_to_library_dxf_with_shell=full_library_path,
                             list_for_import=list_for_import)
    ''''''
    shell_create.create_all_shells(doc = doc_new,
                                   shell_name=shell_name)

    dict_with_list_coordinates_on_side_for_dxf = {'А': {0: {'ВЗ-Н20': [60.0, 50.5]}},
                                                  'Б': {0: {'ВЗ-Н20': [49.0, 29]}},
                                                  'В': {},
                                                  'Г': {},
                                                  'Крышка': {}}

    dict_after_matching = inputs_create.define_matching(dict_with_list_coordinates_on_side_for_dxf)

    ''''''
    inputs_create.create_inputs_in_block(doc = doc_new,
                                         dict_before_match=dict_with_list_coordinates_on_side_for_dxf,
                                         full_shale_name=shell_name,
                                         type_of_explosion='exe')
    ''''''
    dict_with_inserts_inputs = inputs_on_shell.get_shellsidess_input_coordinate(doc = doc_new,
                                                                        dict_after_matching = dict_after_matching,
                                                                        shell_name=shell_name)

    inputs_on_shell.create_inputs_on_topside(doc = doc_new,
                                             dict_with_inserts_inputs = dict_with_inserts_inputs,
                                             shell_name=shell_name)

    inputs_on_topside = search_inputs_on_topside(doc=doc_new,
                                                 shell_name=shell_name)

    move_shells_after_inputs_on_topside(doc = doc_new,
                                        inputs_on_topside=inputs_on_topside)

    shell_create.create_cutside_shell(doc=doc_new,
                                      shell_name=shell_name,
                                      extreme_lines_in_all_blocks=shell_create.define_extreme_lines_in_all_blocks(
                                          doc_new))

    lateral_input_on_side(doc = doc_new,
                          shell_name=shell_name,
                          dict_after_matching=dict_after_matching)

    doc_new.saveas(path_to_save + '\\autotest.dxf')


