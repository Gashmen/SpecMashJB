import ezdxf
'''ИЗМЕРЕНИЕ ДЛИНЫ БЛОКА ПО КООРДИНАТЕ X ПО ГОРИЗОНТАЛЬНЫМ ЛИНИЯМ'''

def check_block_in_doc(doc, block_name):
    '''Проверка нахождения блока в doc, если нет, то выдать ошибку'''
    for block in doc.blocks:
        if block_name == block.dxf.name:
            return True
    else:
        return False

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

def create_dict_with_vertical_lines(block):
    ''' Сначала создаем словарь в котором находится координата y горизантольных линий(ключ) и
        линии на этой координате(значения) в списке. '''
    dict_with_vertical_lines = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'LINE':
            if round(entity.dxf.start[0], 2) == round(entity.dxf.end[0], 2):
                if round(entity.dxf.start[0], 2) not in dict_with_vertical_lines:
                    dict_with_vertical_lines[round(entity.dxf.start[0], 2)] = [entity]
                else:
                    dict_with_vertical_lines[round(entity.dxf.start[0], 2)].append(entity)
    return dict_with_vertical_lines


def calculate_vertical_len_block(block):
    '''
    Считает вертикальную длину блока
    :param block:
    :return:
    '''
    dict_with_horizontal_lines = create_dict_with_horizontal_lines(block=block)
    vertical_len = abs(max(dict_with_horizontal_lines.keys()) - min(dict_with_horizontal_lines.keys()))
    return vertical_len


def calculate_horizontal_len_block(block):
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


if __name__ == '__main__':
    PATH_TO_TERMINAL = 'C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Клеммы\checkcheck.dxf'



