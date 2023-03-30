import ezdxf

from src.dxf_creating import shell_create
from src.dxf_creating import measure_block

def get_scale(scale:float):
    '''Просто получаем масштаб для того, чтобы сделать размер'''
    return scale
def define_inputs_on_topside(doc,shell_name:str):
    '''
    Ищем кабельные ввода вокруг topside
    :param doc: док после добавление кабельнных вводов
    :param shell_name:VP.161610
    :return:{'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    '''

    insert_topside = doc.modelspace().query(f'INSERT[name=="{shell_name}_topside"]')[0]
    extreme_lines_topside = shell_create.define_extreme_lines_in_insert(insert_topside)

    a_side_insert = list()
    b_side_insert = list()
    v_side_insert = list()
    g_side_insert = list()

    for insert_input in doc.modelspace().query('INSERT'):
        if list(insert_input.dxf.insert)[1] == extreme_lines_topside['y_max']:
            if extreme_lines_topside['x_min'] < list(insert_input.dxf.insert)[0] < extreme_lines_topside['x_max']:
                a_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[1] == extreme_lines_topside['y_min']:
            if extreme_lines_topside['x_min'] < list(insert_input.dxf.insert)[0] < extreme_lines_topside['x_max']:
                v_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[0] == extreme_lines_topside['x_min']:
            if extreme_lines_topside['y_min'] < list(insert_input.dxf.insert)[1] < extreme_lines_topside['y_max']:
                g_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[0] == extreme_lines_topside['x_max']:
            if extreme_lines_topside['y_min'] < list(insert_input.dxf.insert)[1] < extreme_lines_topside['y_max']:
                b_side_insert.append(insert_input)
    return {'A_SIDE': a_side_insert,'B_SIDE':b_side_insert,'V_SIDE':v_side_insert,'G_SIDE':g_side_insert}

def calculate_max_up_coordinate(doc, insert_on_side_dict:dict,scale:float):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if 'A_SIDE' in insert_on_side_dict:
        len_inputs = {}
        x_coordinate_inserts ={}
        if insert_on_side_dict['A_SIDE'] !=[]:
            for input_insert in insert_on_side_dict['A_SIDE']:
                name_block = input_insert.dxf.name
                input_block = doc.blocks.get(name_block)
                block_vertical_len = measure_block.calculate_vertical_len_block(input_block)
                if block_vertical_len not in len_inputs:
                    len_inputs[block_vertical_len] = [input_insert]
                else:
                    len_inputs[block_vertical_len].append(input_insert)

                if input_insert.dxf.insert[0] not in x_coordinate_inserts:
                    x_coordinate_inserts[input_insert.dxf.insert[0]] = [input_insert]
                else:
                    x_coordinate_inserts[input_insert.dxf.insert[0]].append(input_insert)
        if len_inputs !={}:

            max_len = max(list(len_inputs.keys()))

            insert_with_min_left_coordinate = x_coordinate_inserts[min(list(x_coordinate_inserts.keys()))][0]

            return (insert_with_min_left_coordinate.dxf.insert[0],insert_with_min_left_coordinate.dxf.insert[1] + max_len/scale)

def calculate_min_down_coordinate(doc, insert_on_side_dict:dict,scale:float):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if 'V_SIDE' in insert_on_side_dict:
        len_inputs = {}
        x_coordinate_inserts ={}
        if insert_on_side_dict['V_SIDE'] !=[]:
            for input_insert in insert_on_side_dict['V_SIDE']:
                name_block = input_insert.dxf.name
                input_block = doc.blocks.get(name_block)
                block_vertical_len = measure_block.calculate_vertical_len_block(input_block)
                if block_vertical_len not in len_inputs:
                    len_inputs[block_vertical_len] = [input_insert]
                else:
                    len_inputs[block_vertical_len].append(input_insert)

                if input_insert.dxf.insert[0] not in x_coordinate_inserts:
                    x_coordinate_inserts[input_insert.dxf.insert[0]] = [input_insert]
                else:
                    x_coordinate_inserts[input_insert.dxf.insert[0]].append(input_insert)
        if len_inputs != {}:
            max_len = max(list(len_inputs.keys()))

            insert_with_min_left_coordinate = x_coordinate_inserts[min(list(x_coordinate_inserts.keys()))][0]

            return (insert_with_min_left_coordinate.dxf.insert[0],insert_with_min_left_coordinate.dxf.insert[1] - max_len/scale)

def calculate_min_left_coordinate(doc, insert_on_side_dict:dict,scale:float):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if 'G_SIDE' in insert_on_side_dict:
        len_inputs = {}
        x_coordinate_inserts ={}
        if insert_on_side_dict['G_SIDE'] !=[]:
            for input_insert in insert_on_side_dict['G_SIDE']:
                name_block = input_insert.dxf.name
                input_block = doc.blocks.get(name_block)
                block_vertical_len = measure_block.calculate_vertical_len_block(input_block)
                if block_vertical_len not in len_inputs:
                    len_inputs[block_vertical_len] = [input_insert]
                else:
                    len_inputs[block_vertical_len].append(input_insert)

                if input_insert.dxf.insert[0] not in x_coordinate_inserts:
                    x_coordinate_inserts[input_insert.dxf.insert[0]] = [input_insert]
                else:
                    x_coordinate_inserts[input_insert.dxf.insert[0]].append(input_insert)
        if len_inputs !={}:
            max_len = max(list(len_inputs.keys()))

            insert_with_min_left_coordinate = x_coordinate_inserts[min(list(x_coordinate_inserts.keys()))][1]

            return (insert_with_min_left_coordinate.dxf.insert[0] - max_len/scale,insert_with_min_left_coordinate.dxf.insert[1])

def calculate_max_right_coordinate(doc, insert_on_side_dict:dict,scale:float):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if 'B_SIDE' in insert_on_side_dict:
        len_inputs = {}
        x_coordinate_inserts ={}
        if insert_on_side_dict['B_SIDE'] !=[]:
            for input_insert in insert_on_side_dict['B_SIDE']:
                name_block = input_insert.dxf.name
                input_block = doc.blocks.get(name_block)
                block_vertical_len = measure_block.calculate_vertical_len_block(input_block)
                if block_vertical_len not in len_inputs:
                    len_inputs[block_vertical_len] = [input_insert]
                else:
                    len_inputs[block_vertical_len].append(input_insert)

                if input_insert.dxf.insert[0] not in x_coordinate_inserts:
                    x_coordinate_inserts[input_insert.dxf.insert[0]] = [input_insert]
                else:
                    x_coordinate_inserts[input_insert.dxf.insert[0]].append(input_insert)
        if len_inputs !={}:
            max_len = max(list(len_inputs.keys()))

            insert_with_min_left_coordinate = x_coordinate_inserts[min(list(x_coordinate_inserts.keys()))][1]

            return (insert_with_min_left_coordinate.dxf.insert[0] - max_len/scale,insert_with_min_left_coordinate.dxf.insert[1])

if __name__ == '__main__':
    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx.dxf')
    scale = get_scale(2.5)
    insert_on_side_dict = define_inputs_on_topside(doc=doc, shell_name='VP.161610')
    point_for_horizontal_dimension =\
        {'max_up':calculate_max_up_coordinate(doc=doc,insert_on_side_dict=insert_on_side_dict,scale=scale),
         'min_up':calculate_min_down_coordinate(doc=doc,insert_on_side_dict=insert_on_side_dict,scale=scale)}

    dim = doc.modelspace().add_aligned_dim(p1=point_for_horizontal_dimension['min_up'],
                                           p2=point_for_horizontal_dimension['max_up'],
                                           dimstyle='EZDXF',
                                           distance = 10)
    print(dim.dimension.get_measurement())
    dim.dimension.dxf.text = f'{round(dim.dimension.get_measurement()*2,2)}'

    doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx_dimesion.dxf')


    # print(point_for_horizontal_dimension)
