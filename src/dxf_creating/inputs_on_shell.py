import os

import ezdxf

from src.dxf_creating import inputs_create,shell_create



def get_tuple_with_inputs_in_side(dict_on_side:dict)->tuple:
    '''
    :param dict_on_side: {0: {'ВЗ-Н20': [33.4, 37.5]}, 1: {'ВЗ-Н20': [86.6, 37.5]}}
    :return: ['VZ-N20','VZ-N20']
    '''

    return_list = list()

    for key, dict_with_inputs_coordinates in dict_on_side.items():
        name_input = inputs_create.return_input_name_in_dict(dict_with_inputs_coordinates) + inputs_create.type_of_explosion_protection('exe')
        if name_input not in return_list:
            return_list.append(name_input)
    return tuple(return_list)

def get_shellsidess_input_coordinate(doc,dict_after_matching:dict,shell_name:str)->dict:
    '''

    :param doc: Док после добавления оболочек и вводов в них во внутрь
    :param dict_after_matching:
    :return:
    '''
    return_dict = dict()
    for side,dict_with_inputs in dict_after_matching.items():
        if dict_with_inputs:
            block_name = shell_name + side
            return_dict[block_name] =[]
            for entity_insert in doc.modelspace().query(f'INSERT[name == "{block_name}"]'):
                for virtual_entity in entity_insert.virtual_entities():
                    if virtual_entity.dxftype() == 'INSERT':
                        if virtual_entity.dxf.name in get_tuple_with_inputs_in_side(dict_with_inputs):
                            return_dict[block_name].append([virtual_entity.dxf.name,virtual_entity.dxf.insert])
    return return_dict

def create_inputs_on_topside(doc,dict_with_inserts_inputs:dict,shell_name:str):

    '''
    УСТАНОВКА НА TOPSIDE вводов
    :param doc:Док после добавления оболочек и вводов в них во внутрь
    :param dict_with_inserts_inputs:
    {'VP.221209_upside': [['VZ-N25_exe', Vec3(145.49293333333335, 59.0, 0.0)],
                        ['VZ-N25_exe', Vec3(115.58626666666669, 59.00000000000001, 0.0)]],
     'VP.221209_downside':[['VZ-N32_exe', Vec3(130.5396, 193.2092, 0.0)]]}
    :param shell_name: VP.161609
    :return: doc
    '''

    insert_name = shell_name + '_topside'
    dict_topside_extreme_coordinate = None
    for insert_topside in doc.modelspace().query(f'INSERT[name == "{insert_name}"]'):
        dict_topside_extreme_coordinate = shell_create.define_extreme_lines_in_insert(insert = insert_topside)

    for side_insert, list_with_inputs_names_coords in dict_with_inserts_inputs.items():

        '''UPSIDE'''
        if 'upside' in side_insert.lower():
            for inputs_names_coords in list_with_inputs_names_coords:
                input_name = inputs_names_coords[0].split('_')[0] + '_withoutcap' #Имя блока под нулевым элементом, но нужно удалить exe
                input_coords = [inputs_names_coords[1][0], dict_topside_extreme_coordinate['y_max']] #По иксу такая же координата, а по
                new_input = doc.modelspace().add_blockref(name = input_name,insert= input_coords)
                new_input.dxf.rotation = 180

        elif 'downside' in side_insert.lower():
            for inputs_names_coords in list_with_inputs_names_coords:
                input_name = inputs_names_coords[0].split('_')[0] + '_withoutcap' #Имя блока под нулевым элементом, но нужно удалить exe
                input_coords = [inputs_names_coords[1][0], dict_topside_extreme_coordinate['y_min']] #По иксу такая же координата, а по
                new_input = doc.modelspace().add_blockref(name = input_name,insert= input_coords)
                new_input.dxf.rotation = 0

        elif 'leftside' in side_insert.lower():
            for inputs_names_coords in list_with_inputs_names_coords:
                input_name = inputs_names_coords[0].split('_')[0] + '_withoutcap' #Имя блока под нулевым элементом, но нужно удалить exe
                input_coords = [dict_topside_extreme_coordinate['x_min'], inputs_names_coords[1][1]] #По иксу такая же координата, а по
                new_input = doc.modelspace().add_blockref(name = input_name,insert= input_coords)
                new_input.dxf.rotation = 270

        elif 'rightside' in side_insert.lower():
            for inputs_names_coords in list_with_inputs_names_coords:
                input_name = inputs_names_coords[0].split('_')[0] + '_withoutcap' #Имя блока под нулевым элементом, но нужно удалить exe
                input_coords = [dict_topside_extreme_coordinate['x_max'], inputs_names_coords[1][1]] #По иксу такая же координата, а по
                new_input = doc.modelspace().add_blockref(name = input_name,insert= input_coords)
                new_input.dxf.rotation = 90

    return doc


if __name__ == '__main__':

    shell_name = 'VP.221209'

    dict_inputs = {'А': {0: {'ВЗ-Н25': [33.4, 37.5]}, 1: {'ВЗ-Н25': [86.6, 37.5]}},
                    'Б': {},
                    'В': {0: {'ВЗ-Н32': [49.0, 37.5]}}, 'Г': {}, 'Крышка': {}}

    dict_after_matching = inputs_create.define_matching(dict_inputs)

    doc = ezdxf.readfile('\\'.join(os.getcwd().split('\\')[0:-1]) + '\\newnewnewn.dxf')

    dict_with_inserts_inputs = get_shellsidess_input_coordinate(doc,
                                        dict_after_matching = dict_after_matching,
                                        shell_name=shell_name)

    create_inputs_on_topside(doc,
                             dict_with_inserts_inputs=dict_with_inserts_inputs,
                             shell_name=shell_name)


    doc.saveas('\\'.join(os.getcwd().split('\\')[0:-1]) +'\\autotest.dxf')

