import ezdxf

from src.dxf_creating import shell_create
from src.dxf_creating import measure_block

def get_scale(scale:float):
    '''Просто получаем масштаб для того, чтобы сделать размер'''
    return scale

def define_inputs_on_topside(doc,shell_name:str,extreme_lines_topside_after_scale):
    '''
    Ищем кабельные ввода вокруг topside
    :param doc: док после добавление кабельнных вводов
    :param shell_name:VP.161610
    :return:{'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    '''

    a_side_insert = list()
    b_side_insert = list()
    v_side_insert = list()
    g_side_insert = list()

    for insert_input in doc.modelspace().query('INSERT'):
        if list(insert_input.dxf.insert)[1] == extreme_lines_topside_after_scale['y_max']:
            if extreme_lines_topside_after_scale['x_min'] < list(insert_input.dxf.insert)[0] < extreme_lines_topside_after_scale['x_max']:
                a_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[0] == extreme_lines_topside_after_scale['x_max']:
            if extreme_lines_topside_after_scale['y_min'] < list(insert_input.dxf.insert)[1] < extreme_lines_topside_after_scale['y_max']:
                b_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[1] == extreme_lines_topside_after_scale['y_min']:
            if extreme_lines_topside_after_scale['x_min'] < list(insert_input.dxf.insert)[0] < extreme_lines_topside_after_scale['x_max']:
                v_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[0] == extreme_lines_topside_after_scale['x_min']:
            if extreme_lines_topside_after_scale['y_min'] < list(insert_input.dxf.insert)[1] < extreme_lines_topside_after_scale['y_max']:
                g_side_insert.append(insert_input)


    return {'A_SIDE': a_side_insert,'B_SIDE':b_side_insert,'V_SIDE':v_side_insert,'G_SIDE':g_side_insert}

def calculate_max_up_coordinate(doc, insert_on_side_dict:dict,scale:float,topside_extreme_lines:dict):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if insert_on_side_dict['A_SIDE']!=[]:

        len_inputs = {}
        x_coordinate_inserts = {}

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

            return [insert_with_min_left_coordinate.dxf.insert[0],insert_with_min_left_coordinate.dxf.insert[1] + max_len/scale]

    else:
        return [topside_extreme_lines['x_min'],topside_extreme_lines['y_max']]


def calculate_min_down_coordinate(doc, insert_on_side_dict:dict,scale:float,topside_extreme_lines:dict):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''

    if insert_on_side_dict['V_SIDE'] !=[]:
        len_inputs = {}
        x_coordinate_inserts = {}
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

            return [insert_with_min_left_coordinate.dxf.insert[0],insert_with_min_left_coordinate.dxf.insert[1] - max_len/scale]
    else:
        return [topside_extreme_lines['x_min'],topside_extreme_lines['y_min']]

def calculate_min_left_coordinate(doc, insert_on_side_dict:dict,scale:float,topside_extreme_lines:dict):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if insert_on_side_dict['G_SIDE'] !=[]:

        len_inputs = {}
        y_coordinate_inserts ={}

        for input_insert in insert_on_side_dict['G_SIDE']:
            name_block = input_insert.dxf.name
            input_block = doc.blocks.get(name_block)
            block_vertical_len = measure_block.calculate_vertical_len_block(input_block)
            if block_vertical_len not in len_inputs:
                len_inputs[block_vertical_len] = [input_insert]
            else:
                len_inputs[block_vertical_len].append(input_insert)

            if input_insert.dxf.insert[0] not in y_coordinate_inserts:
                y_coordinate_inserts[input_insert.dxf.insert[1]] = [input_insert]
            else:
                y_coordinate_inserts[input_insert.dxf.insert[1]].append(input_insert)
        if len_inputs !={}:
            max_len = max(list(len_inputs.keys()))

            insert_with_min_left_coordinate = y_coordinate_inserts[min(list(y_coordinate_inserts.keys()))][0]

            return [insert_with_min_left_coordinate.dxf.insert[0] - max_len/scale,insert_with_min_left_coordinate.dxf.insert[1]]
    else:
        return [topside_extreme_lines['x_min'],topside_extreme_lines['y_min']]

def calculate_max_right_coordinate(doc, insert_on_side_dict:dict,scale:float,topside_extreme_lines:dict):
    '''
    Поиск верхней координаты для выставления размера
    :param doc: док после установки кабельных вводов на топсайд
    :param insert_on_side_list: получается из функции define_inputs_on_topside, список имеет вид:
    {'A_SIDE': [<class 'ezdxf.entities.insert.Insert'> INSERT(#C6C2), <class 'ezdxf.entities.insert.Insert'> INSERT(#C6C6)]
    :return:
    '''
    if insert_on_side_dict['B_SIDE'] !=[]:

        len_inputs = {}
        y_coordinate_inserts ={}

        for input_insert in insert_on_side_dict['B_SIDE']:
            name_block = input_insert.dxf.name
            input_block = doc.blocks.get(name_block)
            block_vertical_len = measure_block.calculate_vertical_len_block(input_block)
            if block_vertical_len not in len_inputs:
                len_inputs[block_vertical_len] = [input_insert]
            else:
                len_inputs[block_vertical_len].append(input_insert)

            if input_insert.dxf.insert[0] not in y_coordinate_inserts:
                y_coordinate_inserts[input_insert.dxf.insert[1]] = [input_insert]
            else:
                y_coordinate_inserts[input_insert.dxf.insert[1]].append(input_insert)
        if len_inputs !={}:
            max_len = max(list(len_inputs.keys()))

            insert_with_max_right_coordinate = y_coordinate_inserts[max(list(y_coordinate_inserts.keys()))][0]

            return [insert_with_max_right_coordinate.dxf.insert[0] + max_len/scale,insert_with_max_right_coordinate.dxf.insert[1]]

    else:
        return [topside_extreme_lines['x_max'],topside_extreme_lines['y_min']]

if __name__ == '__main__':
    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx.dxf')
    scale = get_scale(2.5)
    insert_on_side_dict = define_inputs_on_topside(doc=doc, shell_name='VP.161610')
    point_for_horizontal_dimension =\
        {'max_up':calculate_max_up_coordinate(doc=doc,insert_on_side_dict=insert_on_side_dict,scale=scale),
         'min_down':calculate_min_down_coordinate(doc=doc,insert_on_side_dict=insert_on_side_dict,scale=scale),
         'min_left':calculate_min_left_coordinate()}

    dim = doc.modelspace().add_aligned_dim(p1=point_for_horizontal_dimension['min_up'],
                                           p2=point_for_horizontal_dimension['max_up'],
                                           dimstyle='EZDXF',
                                           distance = 10)
    print(dim.dimension.get_measurement())
    dim.dimension.dxf.text = f'{round(dim.dimension.get_measurement()*2,2)}'

    dim = doc.modelspace().add_aligned_dim(p1=point_for_horizontal_dimension['min_up'],
                                           p2=point_for_horizontal_dimension['max_up'],
                                           dimstyle='EZDXF',
                                           distance=10)
    print(dim.dimension.get_measurement())
    dim.dimension.dxf.text = f'{round(dim.dimension.get_measurement() * 2, 2)}'

    doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx_dimesion.dxf')


    # print(point_for_horizontal_dimension)
