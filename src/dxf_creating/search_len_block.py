import ezdxf

'''Вынесение Hatch у всех block наверх, !белый цвет самый верхний!'''

def set_hatch_before_entity(block):
    block.set_redraw_order(
        (solid.dxf.handle, "%X" % (1000 - solid.dxf.color))
        for solid in block.entity_space if solid.dxftype() == 'HATCH')

'''Получение центра по координате Х'''

def create_dict_with_horizontal_lines(block):
    ''' Сначала создаем словарь в котором находится координата y горизантольных линий(ключ) и
        линии на этой координате(значения) в списке. '''
    dict_with_horizontal_lines = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'LINE':
            if round(entity.dxf.start[1], 2) == round(entity.dxf.end[1],2):
                if round(entity.dxf.start[1], 2) not in dict_with_horizontal_lines:
                    dict_with_horizontal_lines[round(entity.dxf.start[1], 2)] = [entity]
                else:
                    dict_with_horizontal_lines[round(entity.dxf.start[1], 2)].append(entity)
    return dict_with_horizontal_lines

def calculate_terminal_len(block):
    '''
    :param dict_with_horizontal_lines: словарь с линиями полученные после create_dict_with_horizontal
    :return:
    '''
    dict_with_horizontal_lines = create_dict_with_horizontal_lines(block)
    max_sum = []
    for y_coordinate in dict_with_horizontal_lines:
        sum_of_all_lines_in_this_y = 0

        min_x_coord_on_this_horizontal_level_iteration = None
        max_x_coord_on_this_horizontal_level_iteration = None
        '''Найдем самую минимальную координату на этих отрезках и самую максимальную'''

        for line in dict_with_horizontal_lines[y_coordinate]:

            sum_of_all_lines_in_this_y += abs(round(line.dxf.end[0] - line.dxf.start[0], 2))
            if min_x_coord_on_this_horizontal_level_iteration == None and \
                    max_x_coord_on_this_horizontal_level_iteration == None:
                min_x_coord_on_this_horizontal_level_iteration = min(round(line.dxf.end[0], 2),
                                                                     round(line.dxf.start[0], 2))
                max_x_coord_on_this_horizontal_level_iteration = max(round(line.dxf.end[0], 2),
                                                                     round(line.dxf.start[0], 2))

            else:
                min_x_coord_on_this_horizontal_level_iteration = \
                    min(min_x_coord_on_this_horizontal_level_iteration,
                        min(round(line.dxf.end[0], 2), round(line.dxf.start[0], 2)))
                max_x_coord_on_this_horizontal_level_iteration = \
                    max(max_x_coord_on_this_horizontal_level_iteration,
                        max(round(line.dxf.end[0], 2), round(line.dxf.start[0], 2)))

        max_sum.append(max_x_coord_on_this_horizontal_level_iteration - min_x_coord_on_this_horizontal_level_iteration)
    return round(max(max_sum),2)

def calculate_len_din(doc_new,shell_name:str):
    '''
    :param doc_new:
    :param shell_name:VP.110806
    :return:
    '''

    din_reyka = doc_new.blocks[f'DIN_{shell_name}']
    len_dict_reyka = calculate_terminal_len(din_reyka)
    return len_dict_reyka

def measure_vertical_length_input(doc,input_name_after_translit:str):
    '''
    Функция измеряет вертикальную длину кабельного ввода для дальнейшего передвижения блоков между собой
    :param doc: doc после добавления кабельных вводов на стороны
    :param input_name_after_translit: VZ-N25
    :return: Длину инпута : 36,685
    '''
    len_input = 0.0
    for entities_in_input in doc.blocks[f"{input_name_after_translit}_withoutcap"]:
        if entities_in_input.dxftype() == "LINE":
            #Вычленить сначала вертикальные линии
            if round(list(entities_in_input.dxf.end)[1], 2) - round(list(entities_in_input.dxf.start)[1],2) != 0:
                vertical_len = \
                    abs(round(list(entities_in_input.dxf.end)[1], 3)-round(list(entities_in_input.dxf.start)[1], 3))
                len_input = max(len_input,vertical_len)
    return round(len_input,3)

def define_max_length_input(doc,list_inputs_name_after_translit:list[str])->float:
    '''
    Определяем максимальную вертикальную длину среди всех кабельных вводов, которые используются в этом чертеже
    :param doc: текущий док после вставки кабельных вводов на стороны
    :param list_inputs_name_after_translit: ['VZ-N25','VZ-N12']
    :return: Максимальную длину среди них всех :42.685
    '''
    return_value_max_len = 0
    for input_name in list_inputs_name_after_translit:
        return_value_max_len = max(return_value_max_len,
                                   measure_vertical_length_input(doc=doc,input_name_after_translit=input_name))
    return return_value_max_len


if __name__ == '__main__':
    sum_terminal_len = 0
    # doc_terminal = ezdxf.readfile('C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Клеммы\checkcheck.dxf')
    doc_shell = ezdxf.readfile('C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Оболочка\Чертеж4.dxf')
    for block in doc_shell.blocks:
        if 'U28' in block.dxf.name:

            print(block.dxf.name)
            print(calculate_terminal_len(block=block))
            # print(calculate_len_din(doc_new=doc_shell,shell_name=block.dxf.name.split('_')[1]))




    # for block in doc_terminal.blocks:
    #     if '*' not in block.dxf.name:
    #         if len(block.dxf.name.split('_')) == 4:
    #             sum_terminal_len += calculate_terminal_len(block=block)
    # print(sum_terminal_len)

